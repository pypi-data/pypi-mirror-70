"""
Archivematica Client (Gearman Worker)

This executable does the following.

1. Loads tasks from config. Loads a list of performable tasks (client scripts)
   from a config file (typically that in lib/archivematicaClientModules) and
   creates a mapping from names of those tasks (e.g., 'normalize_v1.0') to the
   names of the Python modules that handle them.

2. Registers tasks with Gearman. Creates a Gearman worker and registers the
   loaded tasks with the Gearman server, effectively saying "Hey, I can
   normalize files", etc.

When the MCPServer requests that the MCPClient perform a registered task, the
MCPClient thread calls ``execute_command``, passing it the Gearman job.  This
gets turned into one or more Job objects, each corresponding to a task on the
MCP Server side.  These jobs are sent in batches to the `call()` function of the
Python module configured to handle the registered task type.

The Python modules doing the work receive the list of jobs and set an exit code,
standard out and standard error for each job.  Only one set of jobs executes at
a time, so each Python module is free to assume it has the whole machine at its
disposal, giving it the option of running subprocesses or multiple threads if
desired.

When a set of jobs is complete, the standard output and error of each is written
back to the database.  The exit code of each job is returned to Gearman and
communicated back to the MCP Server (where it is ultimately used to decide which
task to run next).
"""
# This file is part of Archivematica.
#
# Copyright 2010-2017 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.
import configparser
import importlib
import logging
import os
import pickle
import shlex
import time
from functools import partial
from socket import gethostname

import gearman
from django.conf import settings as django_settings
from django.db import transaction

from a3m.client import ASSETS_DIR
from a3m.client import metrics
from a3m.client import MODULES_FILE
from a3m.client.job import Job
from a3m.databaseFunctions import auto_close_db
from a3m.databaseFunctions import getUTCDate
from a3m.databaseFunctions import retryOnFailure
from a3m.main.models import Task


logger = logging.getLogger(__name__)

replacement_dict = {
    r"%sharedPath%": django_settings.SHARED_DIRECTORY,
    r"%clientAssetsDirectory%": ASSETS_DIR,
}


def get_supported_modules():
    """Create and return the ``supported_modules`` dict by parsing the MCPClient
    modules config file (typically MCPClient/lib/archivematicaClientModules).
    """
    supported_modules = {}
    supported_modules_config = configparser.RawConfigParser()
    supported_modules_config.read(MODULES_FILE)
    for client_script, module_name in supported_modules_config.items(
        "supportedBatchCommands"
    ):
        supported_modules[client_script] = module_name
    return supported_modules


@auto_close_db
def handle_batch_task(gearman_job, supported_modules):
    module_name = supported_modules.get(gearman_job.task.decode("utf8"))
    gearman_data = pickle.loads(gearman_job.data)

    utc_date = getUTCDate()
    jobs = []
    for task_uuid in gearman_data["tasks"]:
        task_data = gearman_data["tasks"][task_uuid]
        arguments = task_data["arguments"]

        replacements = list(replacement_dict.items()) + list(
            {
                r"%date%": utc_date.isoformat(),
                r"%taskUUID%": task_uuid,
                r"%jobCreatedDate%": task_data["createdDate"],
            }.items()
        )

        for var, val in replacements:
            arguments = arguments.replace(var, val)

        job = Job(
            gearman_job.task.decode("utf8"),
            task_data["uuid"],
            _parse_command_line(arguments),
            caller_wants_output=task_data["wants_output"],
        )
        jobs.append(job)

    # Set their start times.  If we collide with the MCP Server inserting new
    # Tasks (which can happen under heavy concurrent load), retry as needed.
    def set_start_times():
        Task.objects.filter(taskuuid__in=[item.UUID for item in jobs]).update(
            starttime=utc_date
        )

    retryOnFailure("Set task start times", set_start_times)

    module = importlib.import_module("a3m.client.clientScripts." + module_name)
    module.call(jobs)

    return jobs


def _parse_command_line(s):
    return [_shlex_unescape(x) for x in shlex.split(s)]


# If we're looking at an escaped backtick, drop the escape
# character.  Shlex doesn't do this but bash unescaping does, and we
# want to remain compatible.
def _shlex_unescape(s):
    return "".join(c1 for c1, c2 in zip(s, s[1:] + ".") if (c1, c2) != ("\\", "`"))


def fail_all_tasks(gearman_job, reason):
    gearman_data = pickle.loads(gearman_job.data)

    result = {}

    # Give it a best effort to write out an error for each task.  Obviously if
    # we got to this point because the DB is unavailable this isn't going to
    # work...
    try:

        def fail_all_tasks_callback():
            for task_uuid in gearman_data["tasks"]:
                Task.objects.filter(taskuuid=task_uuid).update(
                    stderror=str(reason), exitcode=1, endtime=getUTCDate()
                )

            retryOnFailure("Fail all tasks", fail_all_tasks_callback)

    except Exception as e:
        logger.exception("Failed to update tasks in DB: %s", e)

    # But we can at least send an exit code back to Gearman
    for task_uuid in gearman_data["tasks"]:
        result[task_uuid] = {"exitCode": 1}

    return pickle.dumps({"task_results": result})


@auto_close_db
def execute_command(supported_modules, gearman_worker, gearman_job):
    """Execute the command encoded in ``gearman_job`` and return its exit code,
    standard output and standard error as a pickled dict.
    """
    logger.debug("\n\n*** RUNNING TASK: %s", gearman_job.task.decode("utf8"))

    with metrics.task_execution_time_histogram.labels(
        script_name=gearman_job.task.decode("utf8")
    ).time():
        try:
            jobs = handle_batch_task(gearman_job, supported_modules)
            results = {}

            def write_task_results_callback():
                with transaction.atomic():
                    for job in jobs:
                        logger.debug("Completed job: %s\n", job.dump())

                        exit_code = job.get_exit_code()
                        end_time = getUTCDate()

                        kwargs = {"exitcode": exit_code, "endtime": end_time}
                        if (
                            django_settings.CAPTURE_CLIENT_SCRIPT_OUTPUT
                            or kwargs["exitcode"] > 0
                        ):
                            kwargs.update(
                                {
                                    "stdout": job.get_stdout(),
                                    "stderror": job.get_stderr(),
                                }
                            )
                        Task.objects.filter(taskuuid=job.UUID).update(**kwargs)

                        results[job.UUID] = {
                            "exitCode": exit_code,
                            "finishedTimestamp": end_time,
                        }

                        if job.caller_wants_output:
                            # Send back stdout/stderr so it can be written to files.
                            # Most cases don't require this (logging to the database is
                            # enough), but the ones that do are coordinated through the
                            # MCP Server so that multiple MCP Client instances don't try
                            # to write the same file at the same time.
                            results[job.UUID]["stdout"] = job.get_stdout()
                            results[job.UUID]["stderror"] = job.get_stderr()

                        if exit_code == 0:
                            metrics.job_completed(gearman_job.task.decode("utf8"))
                        else:
                            metrics.job_failed(gearman_job.task.decode("utf8"))

            retryOnFailure("Write task results", write_task_results_callback)

            return pickle.dumps({"task_results": results})
        except SystemExit:
            logger.error(
                "IMPORTANT: Task %s attempted to call exit()/quit()/sys.exit(). This module should be fixed!",
                gearman_job.task.decode("utf8"),
            )
            return fail_all_tasks(gearman_job, "Module attempted exit")
        except Exception as e:
            logger.exception(
                "Exception while processing task %s: %s",
                gearman_job.task.decode("utf8"),
                e,
            )
            return fail_all_tasks(gearman_job, e)


def start_gearman_worker():
    """Setup a gearman client, for the thread."""
    gm_worker = gearman.GearmanWorker([django_settings.GEARMAN_SERVER])
    host_id = f"{gethostname()}_{os.getpid()}"
    gm_worker.set_client_id(host_id)
    supported_modules = get_supported_modules()
    task_handler = partial(execute_command, supported_modules)
    for client_script in supported_modules:
        gm_worker.register_task(client_script, task_handler)
    fail_max_sleep = 30
    fail_sleep = 1
    fail_sleep_incrementor = 2
    while True:
        try:
            gm_worker.work()
        except gearman.errors.ServerUnavailable as inst:
            logger.error(
                "Gearman server is unavailable: %s. Retrying in %d" " seconds.",
                inst.args,
                fail_sleep,
            )
            metrics.waiting_for_gearman_time_counter.inc(fail_sleep)
            time.sleep(fail_sleep)

            if fail_sleep < fail_max_sleep:
                fail_sleep += fail_sleep_incrementor
        except Exception as e:
            # Generally execute_command should have caught and dealt with any
            # errors gracefully, but we should never let an exception take down
            # the whole process, so one last catch-all.
            logger.exception(
                "Unexpected error while handling gearman job: %s."
                " Retrying in %d seconds.",
                e,
                fail_sleep,
            )
            metrics.waiting_for_gearman_time_counter.inc(fail_sleep)
            time.sleep(fail_sleep)
            if fail_sleep < fail_max_sleep:
                fail_sleep += fail_sleep_incrementor


def main():
    metrics.start_prometheus_server()

    try:
        start_gearman_worker()
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Received keyboard interrupt, quitting.")
