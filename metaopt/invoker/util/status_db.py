"""
Database that keeps track of worker task relations.
"""
from __future__ import division, print_function, with_statement

from metaopt.invoker.util.model import Error, Release, Result, Start, Task
from metaopt.util.stoppable import Stoppable, stoppable_method, stopping_method


class StatusDB(Stoppable):
    """Database that keeps track of worker task relations."""

    def __init__(self, queue_start, queue_task, queue_outcome):
        super(StatusDB, self).__init__()
        self._queue_start = queue_start
        self._queue_task = queue_task
        self._queue_outcome = queue_outcome

        self._call_status_dict = dict()

        # counter for the number of tasks issued via this StatusDB
        self._count_task = 0
        self._count_start = 0
        self._count_outcome = 0

    def _handle_task(self, idle):
        """Handles an initially idle task issued by the invoker."""
        self._call_status_dict[idle.call.id] = idle

    def _handle_start(self, start):
        """Handles a start received from the worker via the status queue."""
        if not isinstance(start, Start):
            raise TypeError("%s objects are not allowed in the start queue" %
                            type(start))

        if start.call.id in self._call_status_dict.keys() and \
                isinstance(self._call_status_dict[start.call.id], Start):
            raise KeyError("Got duplicate start for task %s" % start.call.id +
                           "Make sure IDs are unique.")

        self._call_status_dict[start.call.id] = start

    def _handle_result(self, result):
        """Handles a result received from the worker via the result queue."""

        if result.call.id not in self._call_status_dict.keys():
            raise KeyError("No task to be stopped for ID %s" % result.call.id)

        status = self._call_status_dict[result.call.id]
        if isinstance(status, Result):
            raise ValueError("Got duplicate result for call with id %s." %
                             result.call.id +
                             "Make sure the task ids are unique.")

        self._call_status_dict[result.call.id] = result

    def _handle_error(self, error):
        """Handles an error received from the worker via the result queue."""
        self._call_status_dict[error.call.id] = error

    def _handle_release(self, release):
        for (task_id, status) in self._call_status_dict.iteritems():
            try:
                if release.worker_id == status.worker_id:
                    self._call_status_dict[task_id] = release
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

        if isinstance(outcome, Release):
            self._handle_release(release=outcome)
            return outcome

        raise TypeError("%s objects are not allowed in the result queue" %
                        type(outcome))

    def wait_for_one_task(self):
        """
        Blocks till one task was gotten from the task queue and processed.
        """
        task = self._queue_task.get()
        self._handle_task(task)
        self._count_task += 1
        self._queue_task.task_done()
        return task

    def wait_for_one_start(self):
        """
        Blocks till one start was gotten from the start queue and processed.
        """
        start = self._queue_start.get()
        self._handle_start(start)
        self._count_start += 1
        self._queue_start.task_done()
        return start

    def wait_for_one_outcome(self):
        """
        Blocks till an outcome was gotten from the outcome queue and processed.
        """
        outcome = self._queue_outcome.get()
        self._handle_outcome(outcome)
        self._count_outcome += 1
        self._queue_outcome.task_done()
        return outcome

    def count_running_tasks(self):
        """Returns the number of tasks currently executed by workers."""
        # alternate formulation
        # while len([f for f in self._call_status_dict.values() if t]) > 0:

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
        for [call_id, status] in self._call_status_dict.iteritems():
            if isinstance(status, Task):
                del self._call_status_dict[call_id]
                return status.call

        raise ValueError("No call idling at the moment.")

    def get_idle_call(self, worker_id):
        for status in self._call_status_dict.values():
            if not status.worker_id == worker_id:
                return status  # TODO

    @stoppable_method
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

    @stopping_method
    def stop(self):
        """"""
        self._empty_queue_task()
        assert self._queue_task.empty()
        # issue task done for all unchecked messages of the task queue
        while True:
            try:
                self._queue_task.task_done()
            except Exception:
                # no more task done allowed, we are done here
                break
        self._queue_task.join()

        self._empty_queue_start()
        assert self._queue_start.empty()
        self._queue_start.join()

        # We may have recorded tasks in this database that were never started.
        # This happens when all workers get stopped before one starts the task.
        # So send back a release to the caller for all tasks.
        for task in self._call_status_dict.values():
            if not isinstance(task, Task):
                continue
            release = Release(worker_id=None, call=task.call, value='release')
            self._queue_outcome.put(release)

        while not self._queue_outcome.empty():
            try:
                self._empty_queue_outcome()
            except ValueError:
                # Duplicate result. Should not happen. TODO
                raise ValueError("Got a duplicate outcome." +
                                 "Make sure IDs are unique.")
        self._queue_outcome.join()

    @property
    def outcomes_awaited(self):
        return self._count_task - self._count_outcome
