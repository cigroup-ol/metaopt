"""
Invoker that uses multiple processes.
"""
from __future__ import division, print_function, with_statement

import time
import uuid
from multiprocessing import Manager
from threading import Lock

from metaopt.invoker.base import BaseInvoker
from metaopt.invoker.util.determine_package import determine_package
from metaopt.invoker.util.determine_worker_count import determine_worker_count
from metaopt.invoker.util.model import Error, Finish, Result, Start, Task
from metaopt.invoker.util.task_handle import TaskHandle
from metaopt.invoker.util.worker_provider import WorkerProcessProvider
from metaopt.util.stoppable import stoppable_method, stopping_method
from Queue import Empty


class TimeoutError(BaseException):
    pass


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

        # managed queues common to all worker processes
        manager = Manager()
        self._queue_results = manager.Queue()
        self._queue_status = manager.Queue()
        self._queue_tasks = manager.Queue()

        self._worker_handles = []
        self._worker_task_dict = dict()
        wpp = WorkerProcessProvider(queue_results=self._queue_results,
                                    queue_status=self._queue_status,
                                    queue_tasks=self._queue_tasks)
        self._worker_provider = wpp
        del wpp

        # initialize logging
        #self._logger = multiprocessing.log_to_stderr(logging.INFO)

        # we can not prohibit others to use us in parallel, so
        # make this invoker thread-safe
        self._lock = Lock()

        # set by the pluggable invoker or another caller
        self._f = None  # objective function
        self._param_spec = None  # parameter specification
        self._return_spec = None  # return specification
        self._caller = None  # we call back for each worker result

        super(MultiProcessInvoker, self).__init__()

    @property
    def caller(self):
        """Property for the private caller attribute."""
        with self._lock:
            return self._caller

    @property
    def f(self):
        """Property for the function attribute."""
        with self._lock:
            return self._f

    @f.setter
    def f(self, function):
        """Property for the function attribute."""
        with self._lock:
            self._f = function

    @property
    def param_spec(self):
        """Property for the parameter specification attribute."""
        with self._lock:
            return self._param_spec

    @param_spec.setter
    def param_spec(self, param_spec):
        """Setter for the parameter specification attribute."""
        with self._lock:
            self._param_spec = param_spec

    @property
    def return_spec(self):
        """Property for the return specification attribute."""
        with self._lock:
            return self._return_spec

    @return_spec.setter
    def return_spec(self, return_spec):
        """Setter for the return specification attribute."""
        with self._lock:
            self._return_spec = return_spec

    def _handle_error(self, error):
        self._worker_task_dict[error.worker_id] = None
        try:
            self._caller.on_error(error.value, error.args, **error.kwargs)
        except TypeError:
            # error.kwargs was None
            self._caller.on_error(error.value, error.args, **error.kwargs)

    def _handle_result(self, result):
        self._worker_task_dict[result.worker_id] = None
        self._caller.on_result(result.value, result.args, **result.kwargs)

    def _handle_start(self, start):
        self._worker_task_dict[start.worker_id] = start.task_id

    def _handle_finish(self, finish):
        print(self._worker_handles)  # TODO

        # remove done task
        print(self._worker_task_dict)
        self._worker_task_dict.delete(finish.worker_id)
        print(self._worker_task_dict)  # TODO

        # stop done worker
        for worker_handle in self._worker_handles:
            if (worker_handle.worker_id == finish.worker_id and
                    worker_handle.current_task_id == finish.task_id):
                worker_handle.stop()
                self._worker_handles.remove(worker_handle)

        print(self._worker_handles)  # TODO

    def _wait_for_one_result(self, timeout=None):
        if timeout is None:
            result = self._queue_results.get()
        else:
            try:
                result = self._queue_results.get(timeout=timeout)
            except Empty:
                raise TimeoutError()
        print(result)  # TODO

        # handle successful results
        if isinstance(result, Result):
            self._handle_result(result=result)
            return

        # handle error results
        elif isinstance(result, Error):
            self._handle_error(error=result)
            return

        raise NotImplementedError()

    def _wait_for_start(self, timeout=None):
        while True:
            status = self._queue_status.get()
            # handle worker starting a task
            if isinstance(status, Start):
                self._handle_start(start=status)
                return status.task_id
                break
            # handle worker finishing a task
            elif isinstance(status, Finish):
                self._handle_finish(finish=status)
            raise NotImplementedError()

    @stoppable_method
    def invoke(self, caller, fargs, *vargs, **kwargs):
        """
        Invokes call(f, fargs) with the given function and the given arguments.

        Calls back to self.caller.on_result() for successful invokes.
        Calls back to self.caller.on_error() for unsuccessful invokes.
        Can be called asynchronously, but will block if the call can not be
        executed immediately, especially when using multiple processes/threads.
        """
        with self._lock:
            self._caller = caller

            try:
                # provision one new worker
                worker_handle = self._worker_provider.provision()
                # store the new worker
                self._worker_handles.append(worker_handle)
                self._worker_task_dict[worker_handle.worker_id] = None
            except IndexError:
                # no worker could be provisioned
                pass

            # issue task, the first worker to become idle will execute it
            task = Task(id=uuid.uuid4(),
                        function=determine_package(self._f), args=fargs,
                        param_spec=self._param_spec,
                        return_spec=self._return_spec, kwargs=kwargs)
            self._queue_tasks.put(task)

            # wait for any worker to start working on the task
            # there is always only one task in the queue
            # so the task that gets started is the one we just issued
            task_id = self._wait_for_start()

            # if at worker limit, wait for one result before returning
            if len(self._worker_handles) is self._worker_count_max:
                self._wait_for_one_result(1)

            return TaskHandle(invoker=self, task_id=task_id)

    @stoppable_method
    @stopping_method
    def stop(self):
        """Terminates all worker processes for immediate shutdown."""
        with self._lock:
            for worker_handle in self._worker_handles:
                worker_handle.stop()
                self._worker_handles.remove(worker_handle)

    def stop_task(self, task_id):
        """Terminates a worker_handle given by id."""
        with self._lock:
            for worker_handle in self._worker_handles:
                if self._worker_task_dict[worker_handle.worker_id] != task_id:
                    continue
                worker_handle.stop()
                self._worker_handles.remove(worker_handle)
                return  # worker handle is unique, don't look any further

    def wait(self, timeout=None):
        """Blocks until all workers terminate or the given timeout occurs."""

        start_time = time.time()
        while len(self._worker_handles) > 0:
            try:
                self._wait_for_one_result(1)
            except TimeoutError:
                pass

            if timeout is not None and time.time() - timeout >= start_time:
                raise TimeoutError()
            time.sleep(1)
        return

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()
