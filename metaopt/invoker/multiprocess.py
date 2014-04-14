"""
Invoker that uses multiple processes.
"""
from __future__ import division, print_function, with_statement

import uuid
from multiprocessing import Manager
from threading import Lock

from metaopt.invoker.base import BaseInvoker
from metaopt.invoker.util.determine_package import determine_package
from metaopt.invoker.util.model import Error, Release, Result, Call, Task
from metaopt.invoker.util.status_db import StatusDB
from metaopt.invoker.util.task_handle import CallHandle
from metaopt.invoker.util.worker_provider import WorkerProcessProvider
from metaopt.util.stoppable import stoppable_method, stopping_method,\
    StoppedException
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
        super(MultiProcessInvoker, self).__init__()

        # managed queues common to all worker processes
        self._manager = Manager()
        queue_task = self._manager.Queue(maxsize=1)
        queue_start = self._manager.Queue()
        queue_outcome = self._manager.Queue()

        self._status_db = StatusDB(queue_task=queue_task,
                                   queue_start=queue_start,
                                   queue_outcome=queue_outcome)

        wpp = WorkerProcessProvider(resources=resources,
                                    queue_outcome=queue_outcome,
                                    queue_start=queue_start,
                                    queue_tasks=queue_task,
                                    status_db=self._status_db)
        self._worker_provider = wpp
        del wpp

        # we can not prohibit others to use us in parallel, so
        # make this invoker thread-safe
        self._lock = Lock()

        # set by the pluggable invoker or another caller
        self._f = None  # objective function
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
        assert isinstance(error, Error)
        try:
            self._caller.on_error(error=error.value, fargs=error.call.args,
                                  **error.call.kwargs)
        except TypeError:
            # error.kwargs was None
            self._caller.on_error(error=error.value, fargs=error.call.args)

    def _handle_result(self, result):
        """"""
        assert isinstance(result, Result)
        assert result.value
        assert result.call.args
        assert result.call.kwargs

#         assert (**result.call.kwargs)
        #print((**result.call.kwargs,),)
        self._caller.on_result(value=result.value, fargs=result.call.args,
                 **result.call.kwargs)
        try:
            self._caller.on_result(value=result.value, fargs=result.call.args,
                             **result.call.kwargs)
        except TypeError:
            # result.kwargs was None
            self._caller.on_result(value=result.value, fargs=result.call.args)

    def _handle_release(self, release):
        assert isinstance(release, Release)
        try:
            self._caller.on_error(error=release.value, fargs=release.call.args,
                            **release.call.kwargs)
        except TypeError:
            # error.kwargs was None
            self._caller.on_error(error=release.value, fargs=release.call.args)

    def _handle_outcome(self, outcome):
        """"""
        if isinstance(outcome, Error):
            self._handle_error(error=outcome)
        elif isinstance(outcome, Result):
            self._handle_result(result=outcome)
        elif isinstance(outcome, Release):
            self._handle_release(release=outcome)

    @stoppable_method
    def invoke(self, caller, fargs, **kwargs):
        """
        Invokes call(f, fargs) with the given function and the given arguments.

        Calls back to self._caller.on_result() for successful calls.
        Calls back to self._caller.on_error() for unsuccessful calls.
        Can be called asynchronously, but will block if the call can not be
        executed immediately, especially when using multiple processes/threads.
        """
        self._caller = caller

        # provision one new worker
        try:
            with self._lock:
                self._worker_provider.provision()
        except IndexError:
            # no worker could be provisioned
            pass

        # issue task, the first worker to become idle will execute it
        call = Call(id=uuid.uuid4(),
                    function=determine_package(self._f), args=fargs,
                    kwargs=kwargs)
        task = Task(call=call)
        self._status_db.issue_task(task)

        # wait for any worker to start working on the task
        # there is always only one task in the queue
        # so the task that gets started is the one we just issued
        try:
            _ = self._status_db.wait_for_one_start()
        except EOFError:
            # All workers were stopped before this task was started.
            # That is OK, just return a regular task handle anyway.
            pass

        with self._lock:
            if self._stopped:
                raise StoppedException()

            return CallHandle(invoker=self, call_id=call.id)

    def wait(self):
        """Blocks till all currently invoked tasks terminate."""
        with self._lock:
            while self._status_db.outcomes_awaited > 0:
                # we are still expecting another outcome
                try:
                    outcome = self._status_db.wait_for_one_outcome()
                except IOError as e:
                    # This invoker was stopped via self.stop()
                    # All workers were killed and the queue closed.
                    # We will never get the expected outcome.
                    # That is OK, just do nothing.
                    print(e)
                    return
                self._handle_outcome(outcome=outcome)

    def stop_call(self, call_id):
        """
        Stop a call given by its id, by restarting the executing worker.

        Gets called by a timer in an individual thread.
        """
        with self._lock:
            assert call_id is not None
            self._worker_provider.release(call_id=call_id)
            try:
                self._worker_provider.provision(number_of_workers=1)
            except IndexError:
                # An invoke call provisioned another worker, already.
                # Therefore another worker took the place of the one we killed.
                # That is OK, moving on.
                pass

    @stoppable_method
    @stopping_method
    def stop(self):
        """
        Terminates all worker processes for immediate shutdown.

        Gets called by a timer in an individual thread.
        """
        with self._lock:
            # terminate all workers and handle their release outcomes
            count_workers_killed = self._worker_provider.worker_count
            self._worker_provider.release_all()
            for _ in xrange(count_workers_killed - 1):
                outcome = self._status_db.wait_for_one_outcome()
                self._handle_outcome(outcome=outcome)

            self._status_db.teardown()

            self._manager.shutdown()
