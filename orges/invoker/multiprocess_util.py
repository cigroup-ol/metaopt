"""
Various utilities for the multiprocess invoker.
"""
from __future__ import division, print_function, with_statement

import sys
import uuid
import threading
from collections import namedtuple
from multiprocessing.process import Process

from orges.core.args import call
from orges.util.singleton import Singleton
from orges.invoker.util.determine_worker_count import determine_worker_count


class WorkerProvider(Singleton):
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
        Provision a given number worker processes for future use.
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

            self._workers += worker_processes
        return [WorkerHandle(worker_process) for worker_process in
                worker_processes]

    def release(self, worker_process):
        with self._lock:
            # send manually constructed empty result
            result = Result(worker_id=worker_process.worker_id, function=None,
                            args=None, vargs=None, kwargs=None,
                            task_id=worker_process._current_task_id,
                            value=None)
            worker_process.queue_results.put(result)

            # send kill signal and wait for the process to die
            worker_process.terminate()
            worker_process.join()

            self._workers.remove(worker_process)


class WorkerHandle(object):
    """A means to cancel a worker."""

    def __init__(self, worker):
        self._worker = worker

    @property
    def worker_id(self):
        return self._worker.worker_id

    @property
    def current_task_id(self):
        return self._worker.current_task_id

    def cancel(self):
        """Cancels this worker."""
        WorkerProvider().release(self._worker)


# data structure for results generated by the workers
Task = namedtuple("Task", ["task_id", "function", "args", "vargs", "kwargs"])

# data structure for results generated by the workers
Status = namedtuple("Status", ["task_id", "function", "args", "vargs",
                               "kwargs", "worker_id"])

# data structure for results generated by the workers
Result = namedtuple("Result", ["task_id", "function", "args", "vargs",
                               "kwargs", "worker_id", "value"])


class WorkerProcess(Process):
    """Calls functions with arguments, both given by a queue."""
    def __init__(self, worker_id, queue_results, queue_status,
                 queue_tasks):
        self._worker_id = worker_id
        self._queue_results = queue_results
        self._queue_status = queue_status
        self._queue_tasks = queue_tasks
        self._busy = False
        self._current_task_id = None
        super(WorkerProcess, self).__init__()

    @property
    def worker_id(self):
        """Property for the worker_id attribute of this class."""
        return self._worker_id

    @property
    def queue_tasks(self):
        """Property for the tasks attribute of this class."""
        return self._queue_tasks

    @property
    def queue_status(self):
        """Property for the results attribute of this class."""
        return self._queue_status

    @property
    def queue_results(self):
        """Property for the results attribute of this class."""
        return self._queue_results

    @property
    def busy(self):
        """Property for the results attribute of this class."""
        return self._busy

    @property
    def current_task_id(self):
        """Property for the results attribute of this class."""
        return self._current_task_id

    def run(self):
        """Makes this worker execute all tasks incoming from the task queue."""
        # Get tasks from the queue and trigger their execution
        for task in iter(self.queue_tasks.get, None):
            self._execute(task)

        # send sentinel result back to propagate the end of the task queue
        self._queue_results.put(Result(task_id=None, worker_id=self._worker_id,
                                       function=None, args=None, vargs=None,
                                       kwargs=None, value=None))

    def _execute(self, task):
        self._busy = True
        self._current_task_id = task.task_id
        # announce start of work
        self._queue_status.put(Status(task_id=self._current_task_id,
                                      worker_id=self._worker_id,
                                      function=task.function,
                                      args=task.args, vargs=task.vargs,
                                      kwargs=task.kwargs))

        # import function given by qualified package name
        function = __import__(task.function, globals(), locals(), ['function'],
                              0).f
        # Note that the following is equivalent:
        #from MyPackage.MyModule import f as function

        # make the actual call
        try:
            value = call(function, task.args)
        except Exception:
            value = sys.exc_info()

        # report result back
        self._queue_results.put(Result(task_id=self._current_task_id,
                                       worker_id=self._worker_id,
                                       function=task.function,
                                       args=task.args, value=value,
                                       vargs=task.vargs,
                                       kwargs=task.kwargs))
        self._busy = False
