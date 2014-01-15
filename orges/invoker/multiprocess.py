"""
Invoker that uses multiple processes.
"""
from __future__ import division, print_function, with_statement

import uuid
from time import sleep
from threading import Lock
from multiprocessing import Manager

from orges.invoker.base import BaseInvoker
from orges.util.stoppable import stopping_method, stoppable_method
from orges.invoker.util.task_handle import TaskHandle
from orges.invoker.util.determine_package import determine_package
from orges.invoker.util.determine_worker_count import determine_worker_count
from orges.invoker.util.worker_provider import WorkerProcessProvider
from orges.invoker.util.model import Result, Error, Task


class MultiProcessInvoker(BaseInvoker):
    """
    Invoker that invokes objective functions in parallel using processes.
    """

    def __init__(self, resources=None):
        """
        :param  resources: Number of CPUs to use at most. Will automatically
                           configure itself, if None.
        """

        self._worker_count_max = determine_worker_count(resources)

        # set this using the property
        self._caller = None

        # queues common to all worker processes
        manager = Manager()
        self._queue_results = manager.Queue()
        self._queue_status = manager.Queue()
        self._queue_tasks = manager.Queue()

        self._worker_handles = []
        self._worker_provider = WorkerProcessProvider()

        # initialize logging
        #self._logger = multiprocessing.log_to_stderr(logging.INFO)

        # we can not prohibit others to use us in parallel, so
        # make this invoker thread-safe
        self._lock = Lock()

        super(MultiProcessInvoker, self).__init__(self.caller)

    @property
    def caller(self):
        """Property for the private caller attribute."""
        with self._lock:
            return self._caller

    @caller.setter
    def caller(self, value):
        """Setter for the private caller attribute."""
        with self._lock:
            self._caller = value

    @stoppable_method
    def invoke(self, function, fargs, *vargs, **kwargs):
        """
        Invokes call(f, fargs) with the given function and the given arguments.

        Calls back to self.caller.on_result() for successful invokes.
        Calls back to self.caller.on_error() for unsuccessful invokes.
        Can be called asynchronously, but will block if the call can not be
        executed immediately, especially when using multiple processes/threads.
        """
        with self._lock:
            # try to provision one new worker
            try:
                self._worker_handles.append(self._worker_provider.provision(
                    queue_tasks=self._queue_tasks,
                    queue_results=self._queue_results,
                    queue_status=self._queue_status))
            except IndexError:
                pass  # give the task to one of the busy workers

            # schedule task for any worker to execute
            self._queue_tasks.put(Task(task_id=uuid.uuid4(),
                                       function=determine_package(function),
                                       args=fargs, kwargs=kwargs))

            # wait for any worker to start working on the task
            status = self._queue_status.get()

            if status is None:
                # TODO Why should status be None?
                task_handle = None
            else:
                task_handle = TaskHandle(invoker=self, task_id=status.task_id)

            # if at worker limit, wait for an result
            if len(self._worker_handles) is self._worker_count_max:
                result = self._queue_results.get()

                # handle finished worker
                if result is None:
                    for worker_handle in self._worker_handles:
                        if (
                                worker_handle.worker_id == result.worker_id
                                and worker_handle.current_task_id ==
                                result.task_id):
                            worker_handle.stop()
                            self._worker_handles.remove(worker_handle)

                # handle regular results
                if isinstance(result, Result):
                    self._caller.on_result(result=result.value,
                                           fargs=result.args,
                                           vargs=result.vargs,
                                           **result.kwargs)
                # handle error results
                if isinstance(result, Error):
                    self._caller.on_error(result=result.value,
                                          fargs=result.args,
                                          **result.kwargs)

            return task_handle

    @stoppable_method
    @stopping_method
    def stop(self):
        """Terminates all worker processes for immediate shutdown."""
        with self._lock:
            for worker_handle in self._worker_handles:
                worker_handle.stop()
                self._worker_handles.remove(worker_handle)
            return

    def stop_task(self, task_id):
        """Terminates a worker_handle given by id."""
        with self._lock:
            for worker_handle in self._worker_handles:
                if worker_handle.current_task_id != task_id:
                    continue
                worker_handle.stop()
                self._worker_handles.remove(worker_handle)
                return  # worker handle is unique, don't look any further

    def wait(self):
        """Blocks until all tasks are done."""
        busy = True
        while busy:
            busy = False
            for handle in self._worker_handles:
                if handle.busy:
                    busy = True
                    sleep(0.1)
                    break

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()
