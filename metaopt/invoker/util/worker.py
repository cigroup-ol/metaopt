"""
Utilities around the worker handle.
"""
from __future__ import division, print_function, with_statement

import traceback
from abc import ABCMeta, abstractmethod
from multiprocessing import Process

from metaopt.core.call import call
from metaopt.invoker.util.import_function import import_function
from metaopt.invoker.util.model import Error, Result, Start


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
        self._queue_outcome = queue_results
        self._queue_status = queue_status
        self._queue_task = queue_tasks
        super(WorkerProcess, self).__init__()

    @property
    def worker_id(self):
        """Property for the worker_id attribute of this class."""
        return self._worker_id

    def run(self):
        """Makes this worker execute all tasks incoming from the task queue."""

        while True:
            try:
                self._queue_task.qsize()
            except Exception as e:
                print("Queue.qsize():", e)
                # task queue seems closed, so terminate
                break
            try:
                # get task from the queue, execute task and report back
                task = self._queue_task.get()
                self._execute(task)
                self._queue_task.task_done()
            except EOFError as e:
                # the queue was closed by the invoker, so terminate
                print("Queue.get():", e)
                # task queue seems closed, so terminate
                break

    def _execute(self, task):
        """Executes the given task."""

        # announce start of work
        self._queue_status.put(Start(task_id=task.id,
                                      worker_id=self._worker_id,
                                      function=task.function,
                                      args=task.args,
                                      kwargs=task.kwargs))

        # make the actual call
        try:
            value = call(f=import_function(function=task.function),
                         fargs=task.args, param_spec=task.param_spec,
                         return_spec=task.return_spec)
            self._queue_outcome.put(Result(task_id=task.id,
                                          worker_id=self._worker_id,
                                          function=task.function,
                                          args=task.args, value=value,
                                          kwargs=task.kwargs))
        except Exception as exception:
            # the objective function may raise any exception
            # we can not do anything more helpful than propagate the exception
            # the receiving invoker is another process, so send it as a string
            value = exception
            self._queue_outcome.put(Error(task_id=task.id,
                                          worker_id=self._worker_id,
                                          function=task.function,
                                          args=task.args, value=value,
                                          kwargs=task.kwargs))
