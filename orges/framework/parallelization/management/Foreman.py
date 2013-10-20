"""
Oversights workers.

"""

from __future__ import division
from __future__ import print_function

from multiprocessing import cpu_count
from orges.framework.parallelization.management.LibForeman import \
    fill_worker_pool, send_tasks_to_workers, listen_to_workers


class Foreman(object):
    """
    Oversights some workers, each in a Python process.
    """

    def __init__(self, get_worker, handle_result, handle_error, \
                 get_argument_batches, force_worker_count=None):
        """
        If process_count is None, Foreman will configure itself automatically.

        """
        # (Semi Auto) Configuration
        if force_worker_count is None:
            try:
                self.worker_count = cpu_count()  # number of parallel processes
            except NotImplementedError:
                self.worker_count = 2    # dual cores are very common, now
        else:
            self.worker_count = force_worker_count

        self.get_worker = get_worker()
        self.handle_result = handle_result
        self.handle_error = handle_error
        self.get_argument_batches = get_argument_batches

    def run(self):
        """Makes the workforce to their jobs."""
        # create pool of workers
        worker_pool = fill_worker_pool(self.worker_count, self.get_worker)

        # send tasks to workers
        send_tasks_to_workers(self.get_argument_batches, worker_pool)

        # get results
        listen_to_workers(worker_pool, self.handle_result, self.handle_error)

    def stop(self):
        """Stops the workforce."""
        # TODO implement me
        pass

    def status(self):
        """Reports the status of the workforce."""
        # TODO implement me
        pass
