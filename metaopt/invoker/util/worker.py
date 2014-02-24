"""
Utilities around the worker handle.
"""
from __future__ import division, print_function, with_statement

import traceback
from abc import ABCMeta, abstractmethod
from multiprocessing.process import Process

from metaopt.core.call import call
from metaopt.invoker.util.model import Error, Finish, Result, Start


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
        super(WorkerProcess, self).__init__()

    @property
    def worker_id(self):
        """Property for the worker_id attribute of this class."""
        return self._worker_id

    def run(self):
        """Makes this worker execute all tasks incoming from the task queue."""

        while True:
            # Get tasks from the queue and trigger their execution
            task = None
            try:
                task = self._queue_tasks.get()
            except EOFError:
                # the queue was terminated on the other end by the invoker
                # break, so we can terminate
                break
            finally:
                # always execute task, even if None
                self._execute(task)

    def _execute(self, task):
        """Executes the given task."""

        # announce start of work
        self._queue_status.put(Start(task_id=task.id,
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
            value = call(f=function, fargs=task.args,
                         param_spec=task.param_spec,
                         return_spec=task.return_spec)
            self._queue_results.put(Result(task_id=task.id,
                                          worker_id=self._worker_id,
                                          function=task.function,
                                          args=task.args, value=value,
                                          kwargs=task.kwargs))
        except Exception:
            # the objective function may raise any exception
            # we can not do anything more helpful than propagate the exception
            # the receiving invoker is another process, so send it as a string
            value = traceback.format_exc()
            self._queue_results.put(Error(task_id=task.id,
                                          worker_id=self._worker_id,
                                          function=task.function,
                                          args=task.args, value=value,
                                          kwargs=task.kwargs))

        # announce finish of work to invoker
        self._queue_status.put(Finish(task_id=task.id,
                                      worker_id=self._worker_id,
                                      function=task.function,
                                      args=task.args,
                                      kwargs=task.kwargs))
