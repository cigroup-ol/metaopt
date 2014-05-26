# -*- coding: utf-8 -*-
"""
Various utilities for the multiprocess invoker.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from multiprocessing.synchronize import Lock

# First Party
from metaopt.concurrent.employer.employer import Employer
from metaopt.concurrent.employer.util. \
    determine_worker_count import determine_worker_count
from metaopt.concurrent.employer.util.exception import LayoffError
from metaopt.concurrent.model.call_lifecycle import Layoff
from metaopt.concurrent.worker.process import ProcessWorker


class ProcessWorkerEmployer(Employer):
    """
    Keeps track of up to as many worker processes as there are CPUs.
    """

    # There are a fixed and limited number of CPUs on a computer.
    # These are a shared resource for all process provider instances.
    # So we keep them in a shared space, by implementing the borg pattern.
    _lock = Lock()
    _worker_processes = []

    def __init__(self, queue_tasks, queue_outcome, queue_start,
                 status_db, resources=None):
        """
        :param:    resources    number of (possibly virtual) CPUs to use,
                                defaults to all
        """
        super(ProcessWorkerEmployer, self).__init__()

        with self._lock:
            # use the given queues
            self._queue_outcome = queue_outcome
            self._queue_start = queue_start
            self._queue_task = queue_tasks
            # use up to all CPUs
            self._worker_count_max = determine_worker_count(resources)
            self._status_db = status_db

    @property
    def worker_count_max(self):
        return self._worker_count_max

    def employ(self, number_of_workers=1):
        """
        Employs a given number worker processes for future tasks.
        """
        with self._lock:
            if self._worker_count_max < \
                    (len(self._worker_processes) + number_of_workers):
                raise IndexError("Cannot employ so many worker processes.")

            for _ in range(number_of_workers):
                worker_process = \
                    ProcessWorker(queue_tasks=self._queue_task,
                                  queue_outcome=self._queue_outcome,
                                  queue_start=self._queue_start)
                self._worker_processes.append(worker_process)

    def lay_off(self, call_id, reason=None):
        """
        Lays off the worker process that started the call given by id, if any.

        :param call_id: ID of the call whose executing worker to lay off.
        :param reason: Reason for the lay off. (optional)
        """
        with self._lock:
            try:
                worker_id = self._status_db.get_worker_id(call_id=call_id)
            except KeyError:
                # All workers were killed before one could start the task.
                # The worker for the given task (None) is already terminated.
                # So we have nothing to do here.
                return
            try:
                worker_process = self._get_worker_process_for_id(worker_id)
            except KeyError:
                # nothing to do
                return
            self._lay_off(worker_process, reason)

    def _lay_off(self, worker_process, reason):
        """Lays off the given process workers for the given reason."""

        # send kill signal and wait for the process to die
        # TODO assert worker_process.is_alive()
        worker_process.terminate()
        try:
            worker_process.join()
        except OSError:
            # The worker has already terminated.
            # That is OK, just carry on.
            pass
        self._worker_processes.remove(worker_process)

        try:
            call = self._status_db.get_running_call(worker_process.worker_id)
        except KeyError:
            # The terminated worker was idle
            try:
                call = self._status_db.pop_idle_call()
            except ValueError:
                # No task was started for this worker process.
                # Construct a None "call" manually to use as a dummy pay load.
                call = None

        # send manually constructed layoff outcome
        layoff = Layoff(worker_id=worker_process.worker_id, call=call,
                        value=reason)
        self._queue_outcome.put(layoff)

    def abandon(self, reason=None):
        """
        Lays off all worker processes.
        """
        with self._lock:
            # copy worker processes so that _lay_off does not modify
            if reason is None:
                reason = LayoffError("Releasing all workers.")
            for worker_process in self._worker_processes[:]:
                self._lay_off(worker_process=worker_process, reason=reason)

    def _get_worker_process_for_id(self, worker_id):
        """Utility method to resolve a worker id to a worker process."""
        for worker_process in self._worker_processes:
            if worker_process.worker_id == worker_id:
                return worker_process
        raise KeyError("There is no worker with the given worker id: %s" %
                       worker_id)

    @property
    def worker_count(self):
        """Returns the number of currently running worker processes."""
        with self._lock:
            return len(self._worker_processes)
