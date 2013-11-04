"""
Invoker that uses multiple processes.
"""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

import logging
import multiprocessing
from multiprocessing import Queue, cpu_count

from orges.invoker.base import BaseInvoker
from orges.invoker.multiprocess_lib.Worker import WorkerProcess, Task

# TODO use Pool from multiprocess


class MultiProcessInvoker(BaseInvoker):
    """Invoker that manages worker processes."""

    def __init__(self, resources=None):
        """
        @param resources - number of CPUs to use.
                           will automatically configure itself, if None
        """

        # spawn one worker process per CPU, or as many as requested
        if resources is None:
            try:
                self.worker_count_max = cpu_count()
            except NotImplementedError:
                self.worker_count_max = 2    # dual cores are very common, now
        else:
            self.worker_count_max = resources

        # set this using the property
        self._caller = None

        # init logging
        multiprocessing.log_to_stderr(logging.INFO)

        # queues common to all worker processes
        self.queue_results = Queue()
        self.queue_tasks = Queue()

        # init worker processes
        self._worker_processes = None
        self._populate_worker_processes()

        super(MultiProcessInvoker, self).__init__(resources=resources,
                                                  caller=self._caller)

    def _populate_worker_processes(self):
        """
        Fills this class with as many worker processes with as many as allowed.
        """
        self._worker_processes = []
        for worker_id in range(self.worker_count_max):
            worker_process = WorkerProcess(worker_id=worker_id,
                                           queue_tasks=self.queue_tasks,
                                           queue_results=self.queue_results)
            worker_process.daemon = True  # disallow workers to spawn processes
            worker_process.start()
            self._worker_processes.append(worker_process)

    @property
    def caller(self):
        """Gets the caller."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        self._caller = value

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amout of resources of self."""
        pass

    def invoke(self, f, fargs, **vargs):
        """
        Puts a task into this Invoker's task queue for the workers to execute.
        """
        self.queue_tasks.put(Task(f=f, args=fargs, vargs=vargs))

    def terminate_gracefully(self):
        """Sends sentinel objects to all workers to allow clean shutdown."""
        for worker_process in self._worker_processes:
            worker_process.queue_tasks.put(None)

    def wait(self):
        """
        Blocks till all invoke, on_error or on_result calls are done. Listens
        to the result queue for all workers and dispatches handling.
        """

        self.terminate_gracefully()

        # handle feedback from the workers
        worker_done_count = 0
        while len(self._worker_processes) != worker_done_count:
            # get a message from the queue
            result = self.queue_results.get()

            # handle finished worker
            if result.value == None:
                worker_process = self._worker_processes[result.id]
                worker_process.join()
                self._worker_processes[result.id] = None   # delete reference
                worker_done_count += 1
                break

            # handle all other results
            self._caller.on_result(result.value, result.args, **result.vargs)

    def status(self):
        """Reports the status of the workforce."""
        # TODO implement me
        pass

    def respawn_worker_by_id(self):
        """Terminates and restarts a worker given by id."""
        #TODO implement me
        pass

    def abort(self):
        raise NotImplementedError()
