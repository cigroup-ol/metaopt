"""
Utilities around the worker handle.
"""
from __future__ import division, print_function, with_statement

import traceback
from abc import ABCMeta, abstractmethod
from multiprocessing.process import Process

from orges.core.args import call
from orges.invoker.util.model import Error, Status, Result


class BaseWorker(object):
    """Interface definition for worker implementations."""

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def worker_id(self):
        """Property for the _worker_id attribute."""
        pass


class Worker(BaseWorker):
    """Minimal worker implementation."""

    def __init__(self):
        self._worker_id = None
        super(Worker, self).__init__()

    @property
    def worker_id(self):
        return self._worker_id


class WorkerProcess(Process, Worker):
    """Calls functions with arguments, both given by a queue."""

    def __init__(self, worker_id, queue_results, queue_status,
                 queue_tasks):
        self._worker_id = worker_id
        self._queue_results = queue_results
        self._queue_status = queue_status
        self._queue_tasks = queue_tasks
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
        return self._current_task_id is not None

    @property
    def current_task_id(self):
        """Property for the results attribute of this class."""
        return self._current_task_id

    def run(self):
        """Makes this worker execute all tasks incoming from the task queue."""
        # Get tasks from the queue and trigger their execution
        while True:
            try:
                self._execute(self.queue_tasks.get())
            except EOFError:
                # We just swallowed the poison pill.
                # This means optimizer is finished, so terminate this worker.
                return

    def _execute(self, task):
        """Executes the given task."""
        # send sentinel to propagate the end of the task queue
        if task is None:
            self._queue_results.put(None)
            return

        # announce start of work
        self._current_task_id = task.task_id
        self._queue_status.put(Status(task_id=self._current_task_id,
                                      worker_id=self._worker_id,
                                      function=task.function,
                                      args=task.args,
                                      kwargs=task.kwargs))

        # import function given by qualified package name
        function = __import__(task.function, globals(), locals(), ['function'],
                              0).f
        # Note that the following is equivalent:
        #     from MyPackage.MyModule import f as function
        # Also note this always imports the function "f" as "function".

        # make the actual call
        try:
            value = call(function, task.args)
            self._queue_results.put(Result(task_id=self._current_task_id,
                                          worker_id=self._worker_id,
                                          function=task.function,
                                          args=task.args, value=value,
                                          kwargs=task.kwargs))
        except Exception:
            value = traceback.format_exc()
            self._queue_results.put(Error(task_id=self._current_task_id,
                                          worker_id=self._worker_id,
                                          function=task.function,
                                          args=task.args, value=value,
                                          kwargs=task.kwargs))

        # announce finish of work
        self._current_task_id = None
