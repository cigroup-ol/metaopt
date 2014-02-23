"""
Invoker that uses multiple processes.
"""
from __future__ import division, print_function, with_statement

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
                # provision an new worker
                worker_handle = self._worker_provider.provision()
                # store new worker
                self._worker_handles.append(worker_handle)
                self._worker_task_dict[worker_handle.worker_id] = None
            except IndexError:
                # no worker could be provisioned
                pass  # give the task to one of the busy workers

            # issue task for any worker to execute
            task = Task(id=uuid.uuid4(),
                        function=determine_package(self._f), args=fargs,
                        param_spec=self._param_spec,
                        return_spec=self._return_spec, kwargs=kwargs)
            self._queue_tasks.put(task)

            # wait for any worker to start working on the task
            started = False
            while not started:
                status = self._queue_status.get()
                if status is None:
                    # the worker terminated gracefully
                    assert False
                if isinstance(status, Start):
                    self._worker_task_dict[status.worker_id] = status.task_id
                    assert status.task_id == task.id
                    started = True
                if isinstance(status, Finish):
                    self._worker_task_dict[status.worker_id] = None

            task_handle = TaskHandle(invoker=self, task_id=status.task_id)

            # if at worker limit, wait for an result
            if len(self._worker_handles) is self._worker_count_max:
                result = self._queue_results.get()

                # handle finished worker
                if result is None:
                    for worker_handle in self._worker_handles:
                        if (worker_handle.worker_id == result.worker_id and
                            worker_handle.current_task_id == result.task_id):
                            worker_handle.stop()
                            self._worker_task_dict[status.worker_id] = None
                            self._worker_handles.remove(worker_handle)

                # handle regular results
                if isinstance(result, Result):
                    self._worker_task_dict[status.worker_id] = None
                    self._caller.on_result(result.value, result.args,
                                           **result.kwargs)

                # handle error results
                if isinstance(result, Error):
                    self._worker_task_dict[status.worker_id] = None
                    try:
                        self._caller.on_error(result.value, result.args,
                                              **result.kwargs)
                    except TypeError:
                        # result.kwargs was None
                        self._caller.on_error(result.value, result.args,
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

    def stop_task(self, task_id):
        """Terminates a worker_handle given by id."""
        with self._lock:
            for worker_handle in self._worker_handles:
                if self._worker_task_dict[worker_handle.worker_id] != task_id:
                    continue
                worker_handle.stop()
                self._worker_handles.remove(worker_handle)
                return  # worker handle is unique, don't look any further

    def wait(self):
        """Blocks until all tasks are done."""
        # TODO
        pass

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()
