# -*- coding: utf-8 -*-
"""
Worker implementation that that runs in an own Python Process.

It calls functions with arguments, both of which it gets from a queue.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import pickle
import traceback
import uuid
from multiprocessing import Process
from pickle import PicklingError
from tempfile import TemporaryFile

# First Party
from metaopt.concurrent.model.call_lifecycle import Error, Result, Start
from metaopt.concurrent.worker.util.import_function import import_function
from metaopt.concurrent.worker.worker import Worker
from metaopt.core.call.call import call


class ProcessWorker(Process, Worker):
    """
    Worker implementation that that runs in an own Python Process.

    It calls functions with arguments, both of which it gets from a queue.
    """

    def __init__(self, queue_outcome, queue_start, queue_tasks):
        super(ProcessWorker, self).__init__()
        self._worker_id = uuid.uuid4()
        self._queue_outcome = queue_outcome
        self._queue_start = queue_start
        self._queue_task = queue_tasks

        self.daemon = True  # workers don't spawn processes
        self.start()

    @property
    def worker_id(self):
        """Property for the worker_id attribute of this class."""
        return self._worker_id

    def run(self):
        """Makes this worker execute all tasks incoming from the call queue."""

        while True:
            try:
                self._queue_task.qsize()
            except Exception:
                # call_handle queue seems closed, so terminate
                break
            try:
                # get call_handle from the queue, execute call and report back
                task = self._queue_task.get()
                self._queue_start.put(Start(worker_id=self._worker_id,
                                            call=task.call))
                self._execute(task)
                self._queue_task.task_done()
            except (EOFError, IOError):
                # the queue was closed by the invoker, so terminate
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
