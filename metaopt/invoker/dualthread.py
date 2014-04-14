"""
This module provides a rather simple sequential invoker implementation
"""
from __future__ import division, print_function, with_statement

import uuid
from threading import Lock, Thread

from metaopt.core.call import call
from metaopt.invoker.base import BaseInvoker
from metaopt.invoker.util.task_handle import CallHandle
from metaopt.util.stoppable import stoppable_method, stopping_method


class DualThreadInvoker(BaseInvoker):
    """Invoker that invokes objective functions sequentially."""

    def __init__(self):
        super(DualThreadInvoker, self).__init__()

        self._f = None
        self._param_spec = None
        self._return_spec = None

        self.thread = None
        self.call_handle = None
        self.lock = Lock()

        self.current_task = None
        self.cancelled = False
        self.aborted = False
        self._caller = None  # gets set on invoke

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
            call_id = uuid.uuid4()
            self.call_handle = CallHandle(invoker=self, call_id=call_id)

        self.thread = Thread(target=self.target, args=(caller, self.f, fargs),
                             kwargs=kwargs)
        self.thread.start()

        return self.call_handle

    def target(self, caller, f, fargs, **kwargs):
        """Target function/method for a thread to execute."""
        # TODO Make this a WorkerThread, subclassing multiprocess.Thread.
        # (Symmetrically to the WorkerProcess)
        self._caller = caller
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
            self._caller.on_result(value=value, fargs=fargs, **kwargs)
        else:
            self._caller.on_error(error=error, fargs=fargs, **kwargs)

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
            if self.call_handle is not task:
                return

        with self.lock:
            self.cancelled = True
