"""
Various utilities for the multiprocess invoker.
"""
from __future__ import division, print_function, with_statement

import uuid
from abc import ABCMeta, abstractmethod
from multiprocessing.synchronize import Lock

from orges.invoker.util.determine_worker_count import determine_worker_count
from orges.invoker.util.model import Error
from orges.invoker.util.worker import WorkerProcess
from orges.util.singleton import Singleton
from orges.util.stoppable import Stoppable, stoppable_method, stopping_method


class WorkerProcessProvider(Singleton):
    """
    Keeps track of as many worker processes as there are CPUs.
    """

    def __init__(self, queue_tasks, queue_results, queue_status):
        self._queue_results = queue_results
        self._queue_status = queue_status
        self._queue_tasks = queue_tasks
        self._lock = Lock()
        self._worker_count = determine_worker_count()  # use up to all CPUs
        self._worker_processes = []

    def provision(self, number_of_workers=1):
        """
        Provisions a given number worker processes for future use.

        :rtype: A list of WorkerHandles if number_of_workers > 1,
                otherwise a single WorkerHandle.
        """
        with self._lock:
            if self._worker_count < (len(self._worker_processes) +
                                     number_of_workers):
                raise IndexError("Cannot provision so many worker processes.")

            worker_handles = []
            for _ in range(number_of_workers):
                worker_id = uuid.uuid4()
                worker_process = WorkerProcess(worker_id=worker_id,
                                           queue_tasks=self._queue_tasks,
                                           queue_results=self._queue_results,
                                           queue_status=self._queue_status)
                worker_process.daemon = True  # workers don't spawn processes
                worker_process.start()
                self._worker_processes.append(worker_process)

                worker_handles.append(WorkerProcessHandle(worker_id))

        if number_of_workers > 1:
            return worker_handles
        else:
            return worker_handles[0]

    def release(self, worker_id):
        """Releases a worker process from the work force."""
        with self._lock:
            worker_process = self._get_worker_process_for_id(worker_id)

            # send manually construct error
            result = Error(worker_id=None, task_id=None,
                           function=None, args=None, value=None,
                           kwargs=None)
            self._queue_results.put(result)
            #worker_process.queue_results.join()
            #worker_process.queue_status.join()
            #worker_process.queue_error.join()

            # send kill signal and wait for the process to die
            worker_process.terminate()
            worker_process.join()

            self._worker_processes.remove(worker_process)

    def _get_worker_process_for_id(self, worker_id):
        """Utility method to resolve a worker id to a worker process."""
        for worker_process in self._worker_processes:
            if worker_process.worker_id == worker_id:
                return worker_process
        raise KeyError("There is no worker with the given id.")


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
        raise NotImplementedError()  # Implementations need to overwrite


class WorkerProcessHandle(WorkerHandle):
    """A means to stop a worker."""

    def __init__(self, worker_id):
        super(WorkerProcessHandle, self).__init__()
        self._worker_id = worker_id

    @property
    def worker_id(self):
        """Property for the worker id attribute."""
        return self._worker_id

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this worker."""
        WorkerProcessProvider().release(self._worker_id)
