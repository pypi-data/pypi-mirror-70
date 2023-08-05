from a3m.executeOrRunSubProcess import executeOrRun


def call(jobs):
    for job in jobs:
        with job.JobContext():
            exit_code, std_out, std_error = executeOrRun(
                "command", ["tree"] + job.args[1:], capture_output=True
            )

            job.write_error(std_error)
            job.write_output(std_out)
            job.set_status(exit_code)
