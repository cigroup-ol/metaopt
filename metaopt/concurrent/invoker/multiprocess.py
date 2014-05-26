# -*- coding: utf-8 -*-
"""
Invoker that uses multiple processes.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import uuid
from multiprocessing import Manager
from threading import Lock

# First Party
from metaopt.concurrent.employer.process import ProcessWorkerEmployer
from metaopt.concurrent.invoker.invoker import Invoker
from metaopt.concurrent.invoker.util.call_handle import CallHandle
from metaopt.concurrent.invoker.util.determine_package import determine_package
from metaopt.concurrent.invoker.util.status_db import StatusDB
from metaopt.concurrent.model.call_lifecycle import Call, Error, Layoff, \
    Result, Task
from metaopt.core.stoppable.util.decorator import stoppable, stopping
from metaopt.core.stoppable.util.exception import StoppedError


try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3


class MultiProcessInvoker(Invoker):
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

        # TODO don't
        self._clean_workers = 0
        self._queue_task = queue_task
        self._queue_start = queue_start
        self._queue_outcome = queue_outcome

        self._status_db = StatusDB(queue_task=queue_task,
                                   queue_start=queue_start,
                                   queue_outcome=queue_outcome)

        self._employer = ProcessWorkerEmployer(resources=resources,
                                    queue_outcome=queue_outcome,
                                    queue_start=queue_start,
                                    queue_tasks=queue_task,
                                    status_db=self._status_db)

        # we can not prohibit others to use us in parallel, so
        # make this invoker thread-safe
        self._lock = Lock()

        # set by the pluggable invoker or another caller
        self._f = None  # objective function
        self._param_spec = None  # parameter specification
        self._return_spec = None  # return specification

    def _handle_error(self, error):
        """"""
        assert isinstance(error, Error)
        try:
            self._caller.on_error(value=error.value, fargs=error.call.args,
                                  **error.call.kwargs)
        except TypeError:
            # error.kwargs was None
            self._caller.on_error(value=error.value, fargs=error.call.args)

    def _handle_result(self, result):
        """"""
        assert isinstance(result, Result)
        assert result.value
        assert result.call.args

        try:
            self._caller.on_result(value=result.value, fargs=result.call.args,
                                   **result.call.kwargs)
        except TypeError:
            # result.kwargs was None
            self._caller.on_result(value=result.value, fargs=result.call.args)

    def _handle_layoff(self, layoff):
        assert isinstance(layoff, Layoff)

        try:
            self._caller.on_error(value=layoff.value, fargs=layoff.call.args,
                                  **layoff.call.kwargs)
        except AttributeError:
            # layoff.call was None
            # This means, the WPP constructed the "call" object manually.
            # The caller is not expecting a result for those calls.
            # Nothing to do here.
            return

    def _handle_outcome(self, outcome):
        """"""
        if isinstance(outcome, Error):
            self._handle_error(error=outcome)
        elif isinstance(outcome, Result):
            self._handle_result(result=outcome)
        elif isinstance(outcome, Layoff):
            self._handle_layoff(layoff=outcome)
        else:
            # Will not happen
            raise ValueError("Objects of this type are not allowed in the " +
                             "outcome queue: %s" % type(outcome))

    @stoppable
    def invoke(self, caller, fargs, **kwargs):
        """
        Invokes call(f, fargs) with the given function and the given arguments.

        Calls back to self._caller.on_result() for successful calls.
        Calls back to self._caller.on_error() for unsuccessful calls.
        Can be called asynchronously, but will block if the call can not be
        executed immediately, especially when using multiple processes/threads.
        """
        with self._lock:
            self._caller = caller

            # employ one new worker
            if self._clean_workers <= 0:
                try:
                    self._employer.employ()
                except IndexError:
                    # The worker process provider was at its worker limit, already.
                    # So no new worker could be employed.
                    # We can not assume this invoke's task will be started immediately.
                    # So wait for a free worker by getting and handling an outcome.
                    outcome = self._status_db.wait_for_one_outcome()
                    self._handle_outcome(outcome)

            # issue task, the first worker to become idle will execute it
            call = Call(id=uuid.uuid4(),
                        function=determine_package(self._f), args=fargs,
                        kwargs=kwargs)
            task = Task(call=call)

            try:
                self._status_db.issue_task(task)
                self._clean_workers -= 1
            except StoppedError:
                # The status database was already stopped.
                # This means we are stopped, too.
                # So abort this invoke.
                raise StoppedError()

            # wait for any worker to start working on the task
            # there is always only one task in the queue
            # so the task that gets started is the one we just issued
            try:
                _ = self._status_db.wait_for_one_start()
            except EOFError:
                # All workers were stopped before this task was started.
                # That is OK, just return a regular task handle anyway.
                pass

            if self._stopped:
                raise StoppedError()

            return CallHandle(invoker=self, call_id=call.id)

    def wait(self):
        """Blocks till all currently invoked tasks terminate."""
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
            with self._lock:
                self._handle_outcome(outcome=outcome)

        #self._stop_workers(reason="wait")
        self._clean_workers = self._employer.worker_count_max

    def stop_call(self, call_id, reason):
        """
        Stop a call given by its id, by restarting the executing worker.

        Gets called by a timer in an individual thread.
        """

        assert call_id is not None
        self._employer.lay_off(call_id=call_id, reason=reason)
        try:
            self._employer.employ(number_of_workers=1)
        except IndexError:
            # An invoke call employed another worker, already.
            # Therefore another worker took the place of the one we killed.
            # That is OK, moving on.
            pass

    @stoppable
    @stopping
    def stop(self, reason=None):
        """
        Terminates all worker processes for immediate shutdown.

        Gets called by a timer in an individual thread.
        """
        self._stop_workers(reason=reason)

        self._status_db.stop(reason=reason)

        self._stop_manager()

    def _stop_manager(self):
        try:
            self._manager.shutdown()
        except OSError:
            # The manager has already shutdown.
            # This may happen when all it's queue got closed.
            # That is OK since we wanted to shut it down anyway.
            pass

    def _stop_workers(self, reason):
        # terminate all workers and handle their lay_off outcomes
        count_workers_killed = self._employer.worker_count
        self._employer.abandon()
        for _ in xrange(count_workers_killed - 1):
            outcome = self._status_db.wait_for_one_outcome()
            self._handle_outcome(outcome=outcome)
        #self._employer = ProcessWorkerEmployer(resources=self._resources,
        #                                       queue_outcome=self._queue_outcome,
        #                                       queue_start=self._queue_start,
        #                                       queue_tasks=self._queue_task,
        #                                       status_db=self._status_db)
