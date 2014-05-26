# -*- coding: utf-8 -*-
"""
This module provides a rather simple sequential invoker implementation
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import uuid
from threading import Lock, Thread

# First Party
from metaopt.concurrent.invoker.invoker import Invoker
from metaopt.concurrent.invoker.util.call_handle import CallHandle
from metaopt.core.call.call import call
from metaopt.core.stoppable.stoppable import stoppable
from metaopt.core.stoppable.util.decorator import stopping


class DualThreadInvoker(Invoker):
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
    def f(self, function):
        self._f = function

    @property
    def param_spec(self):
        return self._param_spec

    @param_spec.setter
    def param_spec(self, param_spec):
        self._param_spec = param_spec

    @property
    def return_spec(self):
        return self._return_spec

    @return_spec.setter
    def return_spec(self, return_spec):
        self._return_spec = return_spec

    @stoppable
    def invoke(self, caller, fargs, **kwargs):
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
            self._caller.on_result(value=value, fargs=fargs, **kwargs)
        except Exception as exception:
            self._caller.on_error(value=exception, fargs=fargs, **kwargs)

    def wait(self):
        if self.thread is not None:
            self.thread.join()

        with self.lock:
            aborted = self.aborted

        return aborted

    @stoppable
    @stopping
    def stop(self, reason=None):
        """Stops this invoker."""
        with self.lock:
            self.aborted = True

        self.stop_task(self.current_task, reason=reason)

    def stop_task(self, task, reason=None):
        """Stops the given task."""
        del reason  # TODO
        with self.lock:
            if self.call_handle is not task:
                return

        with self.lock:
            self.cancelled = True
