"""
Invoker that uses multiple processes.
"""
from __future__ import division, print_function, with_statement

import uuid
import logging
import multiprocessing
from threading import Lock
from multiprocessing import Queue, cpu_count

from orges.invoker.base import BaseInvoker
from orges.invoker.multiprocess_util import Task, TaskHandle, WorkerProvider, \
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
                self._worker_count_max = cpu_count()  # configure automatically
            except NotImplementedError:
                self._worker_count_max = 2    # dual cores are very common, now
        else:
            self._worker_count_max = resources

        self._aborted = False

        # set this using the property
        self._caller = None

        # queues common to all worker processes
        self._queue_results = Queue()
        self._queue_status = Queue()
        self._queue_tasks = Queue()

        self._worker_handles = []
        self._worker_provider = WorkerProvider()

        # initialize logging
        self._logger = multiprocessing.log_to_stderr(logging.INFO)

        # we can not prohibit others to use us in parallel, so
        # make this thing thread-safe
        self._lock = Lock()

        super(MultiProcessInvoker, self).__init__(self._caller)

    @property
    def caller(self):
        """Gets the caller."""
        with self._lock:
            return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        with self._lock:
            self._caller = value

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        raise NotImplementedError()

    def invoke(self, function, fargs, *vargs, **kwargs):
        """
        Invokes call(f, fargs) with the given function and the given arguments.

        Calls back to self.caller.on_result() for successful invokes.
        Calls back to self.caller.on_error() for unsuccessful invokes.
        Can be called asynchronously, but will block if the call can not be
        executed immediately, especially when using multiple processes/threads.
        """
        with self._lock:

            #self._logger.warning("invoke entered")

            # provision a new worker, if allowed
            if len(self._worker_handles) is not self._worker_count_max:
                self._worker_handles += self._worker_provider.provision(
                    queue_tasks=self._queue_tasks,
                    queue_results=self._queue_results,
                    queue_status=self._queue_status)

            # schedule task for the workers to execute
            self._queue_tasks.put(Task(task_id=uuid.uuid4(),
                                       function=determine_package(function),
                                       args=fargs, vargs=vargs, kwargs=kwargs))

            # wait for status from a worker
            status = self._queue_status.get()
            if status is None:
                self._aborted = True
                task_handle = None
            else:
                task_handle = TaskHandle(self, status.worker_id,
                                         status.task_id)

            # wait for result, if at worker limit
            if len(self._worker_handles) is self._worker_count_max:
                result = self._queue_results.get()

                # handle finished worker
                if result.value is None:
                    for worker_handle in self._worker_handles:
                        if (
                                worker_handle.worker_id == result.worker_id
                                and worker_handle.current_task_id ==
                                result.task_id):
                            worker_handle.cancel()
                            self._worker_handles.remove(worker_handle)

                # handle all other results

                self._caller.on_result(result=result.value, fargs=result.args,
                                       vargs=result.vargs,
                                       kwargs=result.kwargs)
                # TODO on_error

            #self._logger.warning("invoke left")

            return task_handle, self._aborted

    def abort(self):
        """Terminates all worker processes for immediate shutdown."""

        #self._logger.warning("abort entered")

        # shutdown all workers
        with self._lock:
            for worker_handle in self._worker_handles:
                #print(worker_handle.busy)
                worker_handle.cancel()
                self._worker_handles.remove(worker_handle)
            self._aborted = True

            value = 0
            return (self._aborted, value)

    def terminate_gracefully(self):
        """Sends sentinel objects to all workers to allow clean shutdown."""

        #self._logger.warning("terminate entered")

        with self._lock:
            for _ in self._worker_handles:
                self._queue_tasks.put(None)

    def wait(self):
        """
        Blocks till all invoke, on_error or on_result calls are done. Listens
        to the result queue for all workers and dispatches handling.
        """

        self.terminate_gracefully()

        #self._logger.warning("wait entered")

        #while self._count_busy_workers() >= 1:
            #self._logger.warning(self._count_busy_workers())
        pass

    def cancel(self, worker_id, task_id):
        """Terminates a worker_handle given by id."""
        #self._logger.warning("cancel entered")
        #self._logger.warning(worker_id)

        with self._lock:
            for worker_handle in self._worker_handles:
                if worker_handle.worker_id == worker_id and \
                        worker_handle.current_task_id == task_id:
                    worker_handle.cancel()
                    self._worker_handles.remove(worker_handle)
                    return  # handle is unique, don't look any further
        # TODO: handle queue corruption, by swapping them out for new ones?

        #self._logger.warning("cancel left")

    def status(self):
        """Reports the status of the workforce."""
        # TODO implement me
        pass
