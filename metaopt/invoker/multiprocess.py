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
from metaopt.plugins.util import Invocation


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
        self._count_task = 0
        self._count_outcome = 0

        # managed queues common to all worker processes
        self._manager = Manager()
        self._queue_outcome = self._manager.Queue()
        self._queue_status = self._manager.Queue()
        self._queue_task = self._manager.Queue(maxsize=1)

        #self._worker_handles = []
        wpp = WorkerProcessProvider(queue_results=self._queue_outcome,
                                    queue_status=self._queue_status,
                                    queue_tasks=self._queue_task)
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

    def _handle_error(self, error):
        """"""
        print("MPI._handle_error(%s)" % str(error))

        # TODO This seems redundant.
        # TODO Can't the pluggable invoker construct the invocation itself?
        invocation = Invocation()
        invocation.error = error.value
        invocation.fargs = error.args
        invocation.kwargs = error.kwargs

        print("MPI before _caller.on_error")
        self._caller.on_error(error=error.value, fargs=error.args,
                              invocation=invocation, **error.kwargs)
        print("MPI after _caller.on_error")

    def _handle_result(self, result):
        """"""
        print("MPI._handle_result(%s)" % str(result))
        try:
            self._caller.on_result(result.value, result.args, **result.kwargs)
        except TypeError:
            # outcome.kwargs was None
            self._caller.on_result(result.value, result.args)

    def _handle_outcome(self, outcome):
        """"""
        print("MPI._handle outcome(%s)" % str(outcome))
        if isinstance(outcome, Error):
            print("MPI._handle_outcome before MPI_handle_error")
            self._handle_error(error=outcome)
            print("MPI._handle_outcome after MPI_handle_error")
        elif isinstance(outcome, Result):
            self._handle_result(result=outcome)
        print("MPI._handle_outcome before task_done")
        self._queue_outcome.task_done()
        print("MPI._handle_outcome after task_done")
        print("MPI._handle_outcome before outcome count increment")
        self._count_outcome += 1
        print("MPI._handle_outcome after outcome count increment")

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
                self._worker_provider.provision()
            except IndexError:
                # no worker could be provisioned
                pass

            # issue task, the first worker to become idle will execute it
            task = Task(id=uuid.uuid4(),
                        function=determine_package(self._f), args=fargs,
                        param_spec=self._param_spec,
                        return_spec=self._return_spec, kwargs=kwargs)
            self._queue_task.put(task)
            self._count_task += 1

            # wait for any worker to start working on the task
            # there is always only one task in the queue
            # so the task that gets started is the one we just issued
            self._task_worker_db.wait_for_one_status()

            # if at worker limit, wait for one result before returning
            if self._worker_provider.worker_count() is self._worker_count_max:
                outcome = self._task_worker_db.wait_for_one_outcome()
                self._handle_outcome(outcome)

            return TaskHandle(invoker=self, task_id=task.id)

    @stoppable_method
    @stopping_method
    def stop(self):
        """Terminates all worker processes for immediate shutdown."""
        print("MPI.stop()")
        with self._lock:

            count_workers_killed = self._worker_provider.worker_count()
            self._worker_provider.release_all()
            for _ in xrange(count_workers_killed - 1):
                print("waiting for killed worker:", _)
                outcome = self._task_worker_db.wait_for_one_outcome()
                self._handle_outcome(outcome)

            #for worker_handle in self._worker_handles:
                # stop worker via worker provider
                # this will put an error into the outcome queue
                #worker_handle.stop()
                # the worker provider will issue one error message per stop()
                #print(123123)
                #self._task_worker_db.wait_for_one_outcome()
                # there is noting more to be done with that worker
                # so we can delete it
            #self._worker_handles = []

            print(self._count_task, "+", count_workers_killed, ">", self._count_outcome, "+", self._worker_count_max, "?")
            while self._count_task + count_workers_killed > self._count_outcome + self._worker_count_max:
                self._task_worker_db.wait_for_one_status()
                #self._queue_status.task_done()

            print("MPI.stop before join outcome")
            if not self._queue_outcome.empty():
                outcome = self._queue_outcome.get()
                self._handle_outcome(outcome)
            assert self._queue_outcome.empty()
            self._queue_outcome.join()  # works
            print("MPI.stop after join outcome")

            print("MPI.stop before join status")
            assert self._queue_status.empty()
            self._queue_status.join()  # works
            print("MPI.stop after join status")

            print("MPI.stop before join task")
            assert self._queue_task.empty()
            try:
                self._queue_task.task_done()  # one more for good measure o.0
                pass
            except Exception as e:
                print("e:", e)

            self._queue_task.join()  # fails sometimes
            print("MPI.stop after join task")

            self._manager.shutdown()

    def stop_task(self, task_id):
        """Terminates a worker_handle given by id."""
        with self._lock:
            worker_id = self._task_worker_db.get_worker_id(task_id)
            self._worker_provider.release(worker_id=worker_id)

    def wait(self):
        """Blocks till all currently invoked tasks terminate."""
        print("MPI.wait()")
        with self._lock:
            # empty status queue
            print(self._count_task, ">", self._count_outcome, "?")
            while self._count_task > self._count_outcome:
                print(self._count_task, ">", self._count_outcome)
                outcome = self._task_worker_db.wait_for_one_outcome()
                self._handle_outcome(outcome)

#            found = True
#            while found:
#                found = False
#                if self._queue_status
##            print("MPI.wait() running tasks:", self._task_worker_db.count_running_tasks())
 #           while self._task_worker_db.count_running_tasks() > 0:
 #               print("MPI.wait() running tasks:", self._task_worker_db.count_running_tasks())
 #               try:
 #                   outcome = self._task_worker_db.wait_for_one_outcome()
 #                   self._handle_outcome(outcome)
 #               except Empty:
 #                   continue

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        with self._lock:
            del resources
            raise NotImplementedError()
