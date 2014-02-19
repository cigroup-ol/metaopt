"""
This module provides a rather simple sequential invoker implementation
"""
from __future__ import division, print_function, with_statement

import uuid
from threading import Lock, Thread

from orges.core.call import call
from orges.invoker.base import BaseInvoker
from orges.invoker.util.task_handle import TaskHandle
from orges.util.stoppable import stoppable_method, stopping_method


class DualThreadInvoker(BaseInvoker):
    """Invoker that invokes objective functions sequentially."""

    def __init__(self):
        super(DualThreadInvoker, self).__init__()

        self._f = None
        self._param_spec = None
        self._return_spec = None

        self.thread = None
        self.task = None
        self.lock = Lock()

        self.current_task = None
        self.cancelled = False
        self.aborted = False

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, value):
        self._f = value

    @property
    def param_spec(self):
        return self._param_spec

    @param_spec.setter
    def param_spec(self, value):
        self._param_spec = value

    @property
    def return_spec(self):
        return self._return_spec

    @return_spec.setter
    def return_spec(self, value):
        self._return_spec = value


    @stoppable_method
    def invoke(self, caller, fargs, *vargs, **kwargs):
        with self.lock:
            if self.aborted:
                return None, True

        self.wait()

        with self.lock:
            self.task = TaskHandle(invoker=self, task_id=uuid.uuid4())

        self.thread = Thread(target=self.target, args=(self.f, caller, fargs),
                             kwargs=kwargs)
        self.thread.start()

        return self.task

    def target(self, f, caller, fargs, **kwargs):
        """Target function/method for a thread to execute."""
        # TODO Make this a WorkerThread, subclassing multiprocess.Thread.
        # (Symmetrically to the WorkerProcess)
        try:
            value = call(f, fargs, self.param_spec, self.return_spec)
        except Exception as e:
            with self.lock:
                self.cancelled = True
            error = e

        with self.lock:
            cancelled = self.cancelled
            self.cancelled = False

        if not cancelled:
            caller.on_result(value, fargs, **kwargs)
        else:
            caller.on_error(error, fargs, **kwargs)

    def wait(self):
        if self.thread is not None:
            self.thread.join()

        with self.lock:
            aborted = self.aborted

        return aborted

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this invoker."""
        with self.lock:
            self.aborted = True

        self.stop_task(self.current_task)

    def stop_task(self, task):
        """Stops the given task."""
        with self.lock:
            if self.task is not task:
                return

        with self.lock:
            self.cancelled = True
