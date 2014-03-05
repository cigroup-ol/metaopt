"""
Invoker that uses multiple processes.
"""
from __future__ import division, print_function, with_statement

import uuid
from multiprocessing import Manager
from Queue import Empty
from threading import Lock

from metaopt.invoker.base import BaseInvoker
from metaopt.invoker.util.determine_package import determine_package
from metaopt.invoker.util.determine_worker_count import determine_worker_count
from metaopt.invoker.util.task_handle import TaskHandle
from metaopt.invoker.util.worker_provider import WorkerProcessProvider
from metaopt.util.stoppable import stoppable_method, stopping_method
from metaopt.invoker.util.model import Task, Error, Result
from metaopt.invoker.util.task_worker_db import TaskWorkerDB
from multiprocessing import Queue


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
        self._manager = Manager()
        self._queue_outcome = self._manager.Queue()
        self._queue_status = self._manager.Queue()
        self._queue_tasks = self._manager.Queue()

        #self._queue_outcome = self._manager.Queue()
        #self._queue_status = self._manager.Queue()
        #self._queue_tasks = self._manager.Queue()

        self._worker_handles = []
        wpp = WorkerProcessProvider(queue_results=self._queue_outcome,
                                    queue_status=self._queue_status,
                                    queue_tasks=self._queue_tasks)
        self._worker_provider = wpp
        del wpp

        self._task_worker_db = TaskWorkerDB(queue_outcome=self._queue_outcome,
                                   queue_status=self._queue_status)

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

    def _handle_outcome(self, outcome):
        """"""
        if isinstance(outcome, Error):
            try:
                self._caller.on_error(outcome.value, outcome.args, **outcome.kwargs)
            except TypeError:
                # error.kwargs was None
                self._caller.on_error(outcome.value, outcome.args)
        elif isinstance(outcome, Result):
            try:
                self._caller.on_result(outcome.value, outcome.args, **outcome.kwargs)
            except TypeError:
                # error.kwargs was None
                self._caller.on_result(outcome.value, outcome.args)

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
            self._task_worker_db.wait_for_one_start()

            # if at worker limit, wait for one result before returning
            if len(self._worker_handles) is self._worker_count_max:
                outcome = self._task_worker_db.wait_for_one_outcome()
                print("outcome:", outcome)
                if isinstance(outcome, Result):
                    self._caller.on_result(outcome.value, outcome.args, **outcome.kwargs)
                elif isinstance(outcome, Error):
                    self._caller.on_error(outcome.value, outcome.args, **outcome.kwargs)

            return TaskHandle(invoker=self, task_id=task.id)

    @stoppable_method
    @stopping_method
    def stop(self):
        """Terminates all worker processes for immediate shutdown."""
        with self._lock:
            print(self._worker_handles)
            for worker_handle in self._worker_handles:
                # stop worker via worker provider
                # this will put an error into the outcome queue
                worker_handle.stop()
                # the worker provider will issue one error message per stop()
                print(123123)
                #self._task_worker_db.wait_for_one_outcome()
                # there is noting more to be done with that worker
                # so we can delete it
            self._worker_handles = []

            #self._queue_outcome.close()
            #self._queue_status.close()
            #self._queue_tasks.close()
            #self._manager.shutdown()

    def stop_task(self, task_id):
        """Terminates a worker_handle given by id."""
        with self._lock:
            for worker_handle in self._worker_handles:
                if self._task_worker_db.get_worker_id(task_id) != worker_handle.worker_id:
                    continue
                worker_handle.stop()
                self._worker_handles.remove(worker_handle)
                return  # worker handle is unique, don't look any further

    def wait(self):
        """Blocks till all currently invoked tasks terminate."""
        while self._task_worker_db.count_running_tasks() > 0:
            try:
                self._task_worker_db.wait_for_one_outcome()
            except Empty:
                continue

    def _get_worker_handle(self, worker_id, task_id):
        """Returns the handle from self's worker handles for the given ids."""
        for worker_handle in self._worker_handles:
            if worker_handle.worker_id != worker_id:
                continue
            if self._task_worker_db.get_worker_id(task_id=task_id) != \
                    worker_handle.worker_id:
                continue  # TODO
            return worker_handle
        raise KeyError("No worker handle for worker %s and task %s." %
                       (worker_id, task_id))

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()
