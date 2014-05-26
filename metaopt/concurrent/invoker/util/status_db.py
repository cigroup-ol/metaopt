# -*- coding: utf-8 -*-
"""
Database that keeps track of worker task relations.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import time
from multiprocessing.synchronize import Lock

# First Party
from metaopt.concurrent.model.call_lifecycle import Error, Layoff, Result, \
    Start, Task
from metaopt.core.stoppable.stoppable import Stoppable
from metaopt.core.stoppable.util.decorator import stoppable, stopping
from metaopt.core.stoppable.util.exception import StoppedError


try:
    from Queue import Empty
except ImportError:
    # Queue was renamed to queue in Python 3
    from queue import Empty


class StatusDB(Stoppable):
    """Database that keeps track of worker task relations."""

    def __init__(self, queue_start, queue_task, queue_outcome):
        super(StatusDB, self).__init__()

        # queues for communicating with workers
        self._queue_start = queue_start
        self._queue_task = queue_task
        self._queue_outcome = queue_outcome

        # central data structure this class takes care of
        self._call_status_dict = dict()

        # counter for messages passed through this class
        self._count_task = 0
        self._count_start = 0
        self._count_outcome = 0

        # lock for public methods
        self._lock = Lock()

    def _handle_task(self, idle):
        """Handles an initially idle task issued by the invoker."""
        self._call_status_dict[idle.call.id] = idle

    def _handle_start(self, start):
        """Handles a start received from the worker via the status queue."""
        if not isinstance(start, Start):
            raise TypeError("%s objects are not allowed in the start queue" %
                            type(start))

        try:
            if isinstance(self._call_status_dict[start.call.id], Start):
                raise KeyError("Got duplicate start for task %s" % \
                               start.call.id +
                               "Make sure IDs are unique.")
        except KeyError:
            # There was no entry for this task's uuid in the status database.
            # That is OK, moving on to create one.
            pass

        self._call_status_dict[start.call.id] = start

    def _handle_result(self, result):
        """Handles a result received from the worker via the result queue."""

        if result.call.id not in self._call_status_dict.keys():
            raise KeyError("No task to be stopped for ID %s" % result.call.id)

        status = self._call_status_dict[result.call.id]
        if status == result:
            # nothing to do here
            return

        if isinstance(status, Result):
            raise ValueError("Got duplicate unequal result for call." +
                             "Make sure the call ids are unique:" +
                             "\n    " + repr(result) + "\n    " + repr(status))

        self._call_status_dict[result.call.id] = result

    def _handle_error(self, error):
        """Handles an error received from the worker via the result queue."""
        self._call_status_dict[error.call.id] = error

    def _handle_layoff(self, layoff):
        for (task_id, status) in self._call_status_dict.items():
            try:
                if layoff.worker_id == status.worker_id:
                    self._call_status_dict[task_id] = layoff
            except AttributeError:
                # The status is idle.
                # We do not know the worker, yet.
                # So just check the next status
                continue

    def _handle_outcome(self, outcome):
        """"""
        if isinstance(outcome, Result):
            self._handle_result(result=outcome)
            return outcome

        if isinstance(outcome, Error):
            self._handle_error(error=outcome)
            return outcome

        if isinstance(outcome, Layoff):
            self._handle_layoff(layoff=outcome)
            return outcome

        raise TypeError("%s objects are not allowed in the result queue" %
                        type(outcome))

    @stoppable
    def wait_for_one_task(self):
        """
        Blocks till one task was gotten from the task queue and processed.
        """
        with self._lock:
            task = self._queue_task.get()
            self._handle_task(task)
            self._count_task += 1
            self._queue_task.task_done()
            return task

    @stoppable
    def wait_for_one_start(self):
        """
        Blocks till one start was gotten from the start queue and processed.
        """
        try:
            # TODO this is polling which is bad.
            # Unfortunately this is necessary because of the concurrent stop.
            while True:
                try:
                    start = self._queue_start.get(timeout=1)
                    break
                except Empty:
                    pass
                if self._stopped:
                    raise StoppedError()
        except IOError:
            # The queue was closed before we could read a start.
            # This may happen with fast terminations.
            # The invoker expects an outcome.
            # So send back a manually constructed outcome.
            return Start(worker_id=None, call=None)
        self._handle_start(start)
        self._count_start += 1
        self._queue_start.task_done()
        return start

    @stoppable
    def wait_for_one_outcome(self):
        """
        Blocks till an outcome was gotten from the outcome queue and processed.
        """
        try:
            #outcome = self._queue_outcome.get()

            # TODO this is polling which is bad.
            # Unfortunately this is necessary because of the concurrent stop.
            while True:
                try:
                    outcome = self._queue_outcome.get(timeout=1)
                    break
                except Empty:
                    pass
                if self._stopped:
                    raise StoppedError()

        except EOFError:
            # The outcome queue was closed on the other end.
            # That must have been the queue's manager
            # This means that the invoker tries to stop.
            # So get out of the way.
            return Layoff(worker_id=None, call=None, value=None)

        self._handle_outcome(outcome)
        self._count_outcome += 1
        self._queue_outcome.task_done()
        return outcome

    @stoppable
    def count_running_tasks(self):
        """Returns the number of tasks currently executed by workers."""
        # alternate formulation
        # while len([f for f in self._call_status_dict.values() if t]) > 0:
        with self._lock:
            count = 0
            for status in self._call_status_dict.values():
                if isinstance(status, Start):
                    count += 1
            return count

    def get_worker_id(self, call_id):
        """
        Returns the worker id for a given task id.

        Raises KeyError if there was no worker for that task id. That means,
        all workers were killed before one could start working on the task.
        """
        with self._lock:
            status = self._call_status_dict[call_id]
            return status.worker_id

    def get_running_call(self, worker_id):
        task_found = False
        for status in self._call_status_dict.values():
            try:
                if not status.worker_id == worker_id:
                    continue
            except AttributeError:
                # The status is idle.
                # We do not know the worker, yet.
                # So just check the next status
                continue
            if not isinstance(status, Start):
                continue
            task_found = True
            break

        if not task_found:
            raise KeyError("No status for the worker with id: %s" % worker_id)

        return status.call

    def pop_idle_call(self):
        for [call_id, status] in self._call_status_dict.items():
            if isinstance(status, Task):
                del self._call_status_dict[call_id]
                return status.call

        raise ValueError("No call idling at the moment.")

    def get_idle_call(self, worker_id):
        with self._lock:
            for status in self._call_status_dict.values():
                if not status.worker_id == worker_id:
                    return status  # TODO

    @stoppable
    def issue_task(self, task):
        """"""
        self._queue_task.put(task)
        self._handle_task(task)
        self._count_task += 1

    def _empty_queue_task(self):
        """"""
        # *One* task may got issued after all workers were terminated.
        # So try to get this last task.
        while not self._queue_task.empty():
            task = self.wait_for_one_task()
            self._handle_task(task)

    def _empty_queue_start(self):
        """Empties the start queue, handling all starts."""
        while not self._queue_start.empty():
            start = self.wait_for_one_start()
            self._handle_start(start)

    def _empty_queue_outcome(self):
        """Empties the outcome queue, handling all outcomes."""
        while not self._queue_outcome.empty():
            outcome = self.wait_for_one_outcome()
            self._handle_outcome(outcome)
            #try:
            #
            #except ValueError:
            #    # Duplicate result. Should not happen. TODO
            #    raise ValueError("Got a duplicate outcome. " +
            #                     "Make sure IDs are unique.")

    @stopping
    @stoppable
    def stop(self, reason=None):
        """Stops this status database."""

        # TODO This loop should not be necessary.
        while not self._queue_task.empty():
            self._empty_queue_task()
            time.sleep(0.001)
        assert self._queue_task.empty()

        # issue task done for all unchecked messages of the task queue
        # TODO this should not be necessary
        while True:
            try:
                self._queue_task.task_done()
            except ValueError:
                # no more task done allowed, we are done here
                break
        self._queue_task.join()

        self._empty_queue_start()
        assert self._queue_start.empty()
        self._queue_start.join()

        # We may have recorded a task in this database that was never started.
        # This happens when all workers get stopped before one starts the task.
        # So send back a layoff to the caller for all not yet started tasks.
        for task in self._call_status_dict.values():
            if not isinstance(task, Task):
                continue
            # layoff = Layoff(worker_id=None, call=task.call, value=reason)
            # self._queue_outcome.put(layoff)

        self._empty_queue_outcome()
        assert self._queue_outcome.empty()
        self._queue_outcome.join()

    @property
    def outcomes_awaited(self):
        """
        Returns the number of outcomes that are still awaited.

        Returns 0, if stopped.
        """
        with self._lock:
            if self._stopped:
                return 0

            # Note that we use the start count instead of the the task count.
            # Some issued tasks might never get started if a stop occurs.
            # In that case, no worker will start them.
            # Thus await only started tasks to have a result.
            return self._count_start - self._count_outcome
