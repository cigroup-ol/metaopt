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
from metaopt.invoker.util.model import Error, Release, Result, Task
from metaopt.invoker.util.status_db import StatusDB
from metaopt.invoker.util.task_handle import TaskHandle
from metaopt.invoker.util.worker_provider import WorkerProcessProvider
from metaopt.util.stoppable import stoppable_method, stopping_method,\
    StoppedException
from metaopt.plugins.util import Invocation

try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3


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
        self._queue_start = self._manager.Queue()
        self._queue_task = self._manager.Queue(maxsize=1)

        self._status_db = StatusDB(queue_outcome=self._queue_outcome,
                                            queue_status=self._queue_start)

        wpp = WorkerProcessProvider(queue_outcome=self._queue_outcome,
                                    queue_status=self._queue_start,
                                    queue_tasks=self._queue_task,
                                    status_db=self._status_db)
        self._worker_provider = wpp
        del wpp

        # we can not prohibit others to use us in parallel, so
        # make this invoker thread-safe
        self._lock = Lock()

        # set by the pluggable invoker or another caller
        self._f = None  # objective function

        super(MultiProcessInvoker, self).__init__()
        self._param_spec = None

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
        self._caller.on_error(error=error.value, fargs=error.task.args,
                              **error.task.kwargs)

    def _handle_result(self, result):
        """"""
        assert isinstance(result, Result)
        try:
            self._caller.on_result(result.value, result.task.args, **result.task.kwargs)
        except TypeError:
            # result.kwargs was None
            self._caller.on_result(result.value, result.args)

    def _handle_release(self, release):
        try:
            self._caller.on_error(error=release.value, fargs=release.task.args,
                                  **release.task.kwargs)
        except TypeError:
            self._caller.on_error(error=release.value, fargs=release.task.args,
                                  **release.task.kwargs)

    def _handle_outcome(self, outcome):
        """"""
        if isinstance(outcome, Error):
            self._handle_error(error=outcome)
        elif isinstance(outcome, Result):
            self._handle_result(result=outcome)
        elif isinstance(outcome, Release):
            self._handle_release(release=outcome)
        self._queue_outcome.task_done()
        self._count_outcome += 1

    def _empty_outcome_queue(self):
        """Empties the outcome queue, handling all outcomes."""
        while not self._queue_outcome.empty():
            outcome = self._queue_outcome.get()
            self._handle_outcome(outcome)

    def _empty_status_queue(self):
        """Empties the status queue, handling all """
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
        self._caller = caller

        # if at worker limit, wait for one result before returning
#            if self._worker_provider.worker_count >= self._worker_count_max:
#                outcome = self._status_db.wait_for_one_outcome()
#                self._handle_outcome(outcome)

        try:
            # provision one new worker
            with self._lock:
                self._worker_provider.provision()
        except IndexError:
            # no worker could be provisioned
            pass

        # issue task, the first worker to become idle will execute it
        task = Task(id=uuid.uuid4(),
                    function=determine_package(self._f), args=fargs,
                    kwargs=kwargs)
        self._queue_task.put(task)
        self._count_task += 1

        # wait for any worker to start working on the task
        # there is always only one task in the queue
        # so the task that gets started is the one we just issued
        try:
            self._status_db.wait_for_one_start()
        except EOFError:
            # All workers were stopped before this task was started.
            # That is OK, just return a regular task handle anyway.
            pass

        with self._lock:
            if self._stopped:
                raise StoppedException()

            return TaskHandle(invoker=self, task_id=task.id)

    @stoppable_method
    @stopping_method
    def stop(self):
        """Terminates all worker processes for immediate shutdown.

        Gets called by a timer in an individual thread."""
        with self._lock:
            # terminate all workers and handle their release outcomes
            count_workers_killed = self._worker_provider.worker_count
            self._worker_provider.release_all()
            for _ in xrange(count_workers_killed - 1):
                outcome = self._status_db.wait_for_one_outcome()
                self._handle_outcome(outcome)

#             while self._count_task + count_workers_killed > \
#                     self._count_outcome + self._worker_count_max:
#                 self._status_db.wait_for_one_start()

            self._empty_outcome_queue()
            assert self._queue_outcome.empty()
            self._queue_outcome.join()

            assert self._queue_start.empty()
            self._queue_start.join()

            # *One* task may got issued after all workers were terminated.
            # So try to get this last task.
            if not self._queue_task.empty():
                task = self._queue_task.get()
            assert self._queue_task.empty()

            # issue task done for all unchecked messages of the task queue
            while True:
                try:
                    self._queue_task.task_done()
                except Exception as e:
                    # no more task done allowed, we are done here
                    break
            self._queue_task.join()

            self._manager.shutdown()

    def stop_task(self, task_id):
        """
        Terminates a worker_handle given by id.

        Gets called by a timer in an individual thread.
        """
        #print(self._status_db.count_running_tasks())
        with self._lock:
            assert task_id is not None
            self._worker_provider.release(task_id=task_id)
            try:
                self._worker_provider.provision(number_of_workers=1)
            except IndexError:
                # A call to invoke caused another worker to be provisioned already.
                # That is OK.
                pass

    def wait(self):
        """Blocks till all currently invoked tasks terminate."""
        with self._lock:
            while self._count_task > self._count_outcome:
                # we are still expecting another outcome
                try:
                    outcome = self._status_db.wait_for_one_outcome()
                except IOError:
                    # This invoker was stopped via self.stop()
                    # All workers were killed and the queue closed.
                    # We will never get the expected outcome.
                    # That is OK, just do nothing.
                    return
                self._handle_outcome(outcome)

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        with self._lock:
            del resources
            raise NotImplementedError()
