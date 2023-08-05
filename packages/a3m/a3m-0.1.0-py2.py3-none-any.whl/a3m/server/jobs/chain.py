"""
Job chain logic.

The `JobChain` class determines which job should be run next, based on
the workflow and the exit code of the previous job. It also stores context
provided by previous jobs in the same chain (e.g. choices for a decision).

This module knows about all `Job` subclasses, and will instantiate the correct
one by looking at the workflow.
"""
import logging

from django.utils import timezone

from a3m.server.jobs.client import ClientScriptJob
from a3m.server.jobs.client import DirectoryClientScriptJob
from a3m.server.jobs.client import FilesClientScriptJob
from a3m.server.jobs.decisions import NextChainDecisionJob
from a3m.server.jobs.decisions import UpdateContextDecisionJob
from a3m.server.jobs.local import GetUnitVarLinkJob
from a3m.server.jobs.local import SetUnitVarLinkJob


logger = logging.getLogger(__name__)


def get_job_class_for_link(link):
    """Return the appropriate `Job` class to be used for the workflow link.

    Keys off of the `@manager` config option, which referenced the previous
    linkTaskManager implementation.
    """
    manager_name = link.config["@manager"]
    if manager_name == "linkTaskManagerDirectories":
        job_class = DirectoryClientScriptJob
    elif manager_name == "linkTaskManagerFiles":
        job_class = FilesClientScriptJob
    elif manager_name == "linkTaskManagerChoice":
        job_class = NextChainDecisionJob
    elif manager_name == "linkTaskManagerReplacementDicFromChoice":
        job_class = UpdateContextDecisionJob
    elif manager_name == "linkTaskManagerSetUnitVariable":
        job_class = SetUnitVarLinkJob
    elif manager_name == "linkTaskManagerUnitVariableLinkPull":
        job_class = GetUnitVarLinkJob
    else:
        raise ValueError(f"Unknown manager type {manager_name}")

    return job_class


class JobChain:
    """
    Creates jobs as necessary based on the workflow chain and package given.

    Intended to be used as an iterator that returns jobs (e.g.
    `job = next(JobChain(...))`).

    Job chains are used for passing information between jobs, via:
        * context, a dict of replacement variables for tasks
        * next_link, a workflow link that can be set to redirect the job chain
    """

    def __init__(self, package, chain, workflow, starting_link=None):
        """Create an instance of a chain, based on the workflow chain given."""
        self.package = package
        self.chain = chain
        self.workflow = workflow
        self.started_on = timezone.now()

        self.initial_link = starting_link or self.chain.link
        self.current_link = None
        self.next_link = self.initial_link

        self.current_job = None
        # TODO: package context hits the db, make that clearer
        self.context = self.package.context.copy()

        logger.debug(
            "Creating JobChain %s for package %s (initial link %s)",
            chain.id,
            package.uuid,
            self.initial_link,
        )

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_link:
            next_link = self.next_link
            self.next_link = None
        else:
            try:
                next_link = self.current_link.get_next_link(self.current_job.exit_code)
            except KeyError:
                next_link = None

        if next_link:
            self.current_link = next_link
            job_class = get_job_class_for_link(self.current_link)
            self.current_job = job_class(self, self.current_link, self.package)
            return self.current_job
        else:
            self.current_link = None
            self.current_job = None
            self.chain_completed()
            raise StopIteration

    @property
    def id(self):
        return self.chain.id

    def job_completed(self):
        logger.debug(
            "%s %s done with exit code %s",
            self.current_job.__class__.__name__,
            self.current_job.uuid,
            self.current_job.exit_code,
        )
        if isinstance(self.current_job, ClientScriptJob):
            self.current_job.update_status_from_exit_code()
        else:
            self.current_job.mark_complete()

    def chain_completed(self):
        """Log chain completion
        """
        logger.debug(
            "Done with chain %s for package %s", self.chain.id, self.package.uuid
        )
