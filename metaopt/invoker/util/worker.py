"""
Utilities around the worker handle.
"""
from __future__ import division, print_function, with_statement

import pickle
import traceback
from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from pickle import PicklingError
from tempfile import TemporaryFile

from metaopt.core.call import call
from metaopt.invoker.util.import_function import import_function
from metaopt.invoker.util.model import Error, Result, Start, Call


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

    def __init__(self, worker_id, queue_outcome, queue_start,
                 queue_tasks):
        self._worker_id = worker_id
        self._queue_outcome = queue_outcome
        self._queue_start = queue_start
        self._queue_task = queue_tasks
        super(WorkerProcess, self).__init__()

    @property
    def worker_id(self):
        """Property for the worker_id attribute of this class."""
        return self._worker_id

    def run(self):
        """Makes this worker execute all tasks incoming from the call_handle queue."""

        while True:
            try:
                self._queue_task.qsize()
            except Exception:
                #print("Queue.qsize():", e)
                # call_handle queue seems closed, so terminate
                break
            try:
                # get call_handle from the queue, execute call_handle and report back
                task = self._queue_task.get()
                self._queue_start.put(Start(worker_id=self._worker_id,
                                            call=task.call))
                self._execute(task)
                self._queue_task.task_done()
            except EOFError:
                # the queue was closed by the invoker, so terminate
                #print("Queue.get():", e)
                # call_handle queue seems closed, so terminate
                break

    def _execute(self, task):
        """Executes the given call_handle."""

        # make the actual call
        function = import_function(function=task.call.function)
        try:
            try:
                value = call(f=function, fargs=task.call.args,
                             param_spec=function.param_spec,
                             return_spec=function.return_spec)
            except AttributeError:
                # function had no return type specification
                value = call(f=function, fargs=task.call.args,
                             param_spec=function.param_spec)
            self._queue_outcome.put(Result(worker_id=self._worker_id,
                                           call=task.call,
                                           value=value))
        except Exception as value:
            # the objective function may raise any exception
            # we can not do anything more helpful than propagate the exception
            # we need to send the exception to the main process via a queue
            # we need to make sure the exception is pickleable for the queue
            # so test pickleability and fall back to sending the exception

            with TemporaryFile() as tmp_file:
                try:
                    pickle.dump(value, tmp_file)
                except PicklingError:
                    value = traceback.format_exc()

            self._queue_outcome.put(Error(worker_id=self._worker_id,
                                          call=task.call,
                                          value=value))
