"""
Means to stop tasks for invokers.
"""
from __future__ import division, print_function, with_statement

from metaopt.util.stoppable import Stoppable, stoppable_method, stopping_method


class CallHandle(Stoppable):
    """A means to stopped a task."""

    def __init__(self, invoker, call_id):
        self._invoker = invoker
        self._call_id = call_id
        super(CallHandle, self).__init__()

    @stoppable_method
    @stopping_method
    def stop(self):
        """Cancels the worker executing this task."""
        self._invoker.stop_call(call_id=self._call_id)
