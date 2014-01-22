"""
Various utilities for the multiprocess invoker.
"""
from __future__ import division, print_function, with_statement

import uuid
import threading
from abc import ABCMeta, abstractmethod

from orges.util.singleton import Singleton
from orges.util.stoppable import Stoppable, stopping_method, stoppable_method
from orges.invoker.util.model import Error
from orges.invoker.util.worker import WorkerProcess
from orges.invoker.util.determine_worker_count import determine_worker_count


class WorkerProcessProvider(Singleton):
    """
    Keeps track of as many worker processes as there are CPUs.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._worker_count = determine_worker_count()  # use up to all CPUs
        self._workers = []

    def provision(self, queue_tasks, queue_results, queue_status,
                  number_of_workers=1):
        """
        Provisions a given number worker processes for future use.

        :rtype: A list of WorkerHandles if number_of_workers > 1,
                otherwise a single WorkerHandle.
        """
        with self._lock:
            if self._worker_count < (len(self._workers) + number_of_workers):
                raise IndexError("Cannot provision so many worker processes.")

            worker_processes = []
            for _ in range(number_of_workers):
                worker_id = uuid.uuid4()
                worker_process = WorkerProcess(worker_id=worker_id,
                                               queue_tasks=queue_tasks,
                                               queue_results=queue_results,
                                               queue_status=queue_status)
                worker_process.daemon = True  # workers don't spawn processes
                worker_process.start()
                worker_processes.append(worker_process)

            self._workers.extend(worker_processes)
        if number_of_workers > 1:
            return [WorkerProcessHandle(worker_process) for worker_process in
                    worker_processes]
        else:
            return WorkerProcessHandle(worker_processes[0])

    def release(self, worker_process):
        """Releases a worker process from the work force."""
        with self._lock:
            # send manually construct error
            result = Error(worker_id=worker_process.worker_id,
                           function=None,
                           args=None, kwargs=None,
                           task_id=worker_process.current_task_id,
                           value=None)
            worker_process.queue_results.put(result)

            # send kill signal and wait for the process to die
            worker_process.terminate()
            worker_process.join()

            self._workers.remove(worker_process)


class WorkerHandle(Stoppable):
    """Interface definition for worker handle implementations."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        super(WorkerHandle, self).__init__()

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this worker."""
        raise NotImplementedError  # Implementations need to handle this


class WorkerProcessHandle(WorkerHandle):
    """A means to stop a worker."""

    def __init__(self, worker_process):
        super(WorkerProcessHandle, self).__init__()
        self._worker_process = worker_process

    @property
    def worker_id(self):
        """Property for the worker_id attribute of this handle's worker."""
        return self._worker_process.worker_id

    @property
    def current_task_id(self):
        """Property for the current_task_id of this handle's worker."""
        return self._worker_process.current_task_id

    @property
    def busy(self):
        """Property for the busy attribute of this handle's worker."""
        return self._worker_process.busy

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this worker."""
        WorkerProcessProvider().release(self._worker_process)
