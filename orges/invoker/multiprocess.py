"""
Invoker that uses multiple processes.
"""
from __future__ import division, print_function, with_statement

import logging
import multiprocessing
from multiprocessing import Queue, cpu_count
import uuid

from orges.invoker.base import BaseInvoker

from orges.invoker.multiprocess_util import WorkerProvider, Task, TaskHandle, \
    determine_package

# TODO use Pool from multiprocess
# TODO ensure tasks can be cancelled that are waiting in the queue


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
                self.worker_count_max = cpu_count()  # configure automatically
            except NotImplementedError:
                self.worker_count_max = 2    # dual cores are very common, now
        else:
            self.worker_count_max = resources

        #self.worker_count_max = 1  # TODO

        self.aborted = False

        # set this using the property
        self._caller = None

        # initialize logging
        self._logger = multiprocessing.log_to_stderr(logging.INFO)

        # queues common to all worker processes
        self._queue_results = Queue()
        self._queue_status = Queue()
        self._queue_tasks = Queue()

        # init worker processes
        self._worker_processes = []
        self._worker_provider = WorkerProvider()
        #self._populate_worker_processes()

        super(MultiProcessInvoker, self).__init__(resources=resources,
                                                  caller=self._caller)

    @property
    def caller(self):
        """Gets the caller."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        self._caller = value

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        raise NotImplementedError()

    def invoke(self, function, fargs, **vargs):
        """
        Invokes call(f, fargs) with the given function and the given arguments.

        Calls back to self.caller.on_result() for successful invokes.
        Calls back to self.caller.on_error() for unsuccessful invokes.
        Can be called asynchronously, but will block if the call can not be
        executed immediately, especially when using multiple processes/threads.
        """
        #self._logger.warning("invoke entered")

        # provision a new worker, if allowed
        if len(self._worker_processes) is not self.worker_count_max:
            self._worker_processes += self._worker_provider.provision(
                     queue_tasks=self._queue_tasks,
                     queue_results=self._queue_results,
                     queue_status=self._queue_status)

        # schedule task for the workers to execute
        self._queue_tasks.put(Task(task_id=uuid.uuid4(),
                                   f_package=determine_package(function),
                                   args=fargs, vargs=vargs))

        # wait for status from a worker
        status = self._queue_status.get()
        if status is None:
            self.aborted = True
            task_handle = None
        else:
            task_handle = TaskHandle(self, status.worker_id, status.task_id)

        # wait for result, if at worker limit
        if len(self._worker_processes) is self.worker_count_max:
            result = self._queue_results.get()

            # handle finished worker
            if result.value is None:
                worker_process = self._worker_processes[result.worker_id]
                self._worker_provider.release(worker_process)

            # handle all other results
            self._caller.on_result(result.value, result.args, **result.vargs)

        #self._logger.warning("invoke left")

        return task_handle, self.aborted

    def abort(self):
        """Terminates all worker processes for immediate shutdown."""

        #self._logger.warning("abort entered")

        # shutdown all workers
        for worker_process in self._worker_processes:
            print(worker_process.busy)
            worker_process.terminate()
            worker_process.join()
        self.aborted = True

        value = 0
        return (self.aborted, value)

    def terminate_gracefully(self):
        """Sends sentinel objects to all workers to allow clean shutdown."""

        #self._logger.warning("terminate entered")

        for worker_process in self._worker_processes:
            worker_process.queue_tasks.put(None)

    def _count_busy_workers(self):
        #self._logger.warning("count busy workers entered")

        worker_busy_count = 0
        for worker_process in self._worker_processes:
            if worker_process.busy:
                worker_busy_count += 1
        #self._logger.warning(worker_busy_count)
        return worker_busy_count

    def wait(self):
        """
        Blocks till all invoke, on_error or on_result calls are done. Listens
        to the result queue for all workers and dispatches handling.
        """

        #self.terminate_gracefully()

        #self._logger.warning("wait entered")

        while self._count_busy_workers() >= 1:
            #self._logger.warning(self._count_busy_workers())
            pass

    def cancel(self, worker_id, task_id):
        """Terminates a worker given by id."""
        #self._logger.warning("cancel entered")
        #self._logger.warning(worker_id)

        for worker_process in self._worker_processes:
            if worker_process.worker_id == worker_id and \
                    worker_process.current_task_id == task_id:
                self._remove_worker_process(worker_process)
                return  # worker id is unique, no need to look any further
        # TODO: handle queue corruption, by swapping them out for new ones?

        #self._logger.warning("cancel left")

    def status(self):
        """Reports the status of the workforce."""
        # TODO implement me
        pass
