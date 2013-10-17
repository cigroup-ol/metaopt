"""
Oversights workers.

"""

from __future__ import division
from __future__ import print_function

from collections import namedtuple
from multiprocessing import cpu_count
from orges.parallelization.management.LibForeman import fill_worker_pool,\
    send_tasks, listen_to_workers

class Foreman(object):
    """
    Oversights some workers, each in a Python process.
    """

    @callable
    def __init__(self, worker, result_handler, args_generator, \
                 force_worker_count=None):
        """
        If process_count is None, Foreman will configure itself automatically.

        """
        # (Semi Auto) Configuration
        if force_worker_count is None:
            try:
                self.worker_count = cpu_count()    # number of parallel processes
            except NotImplementedError:
                self.worker_count = 2    # dual cores are very common, now
        else:
            self.worker_count = force_worker_count

        self.worker = worker
        self.handle_result = result_handler
        self.args_generator = args_generator

    def run(self):
        # create pool of workers
        worker_pool = fill_worker_pool(self.worker_count, self.worker)

        # send tasks to workers
        send_tasks(worker_pool, self.args_generator)

        # get results
        listen_to_workers(worker_pool, self.handle_result)
