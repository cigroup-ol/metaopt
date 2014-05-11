# -*- coding: utf-8 -*-
"""
Means to stop tasks for invokers.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.employer.util.exception import LayoffException
from metaopt.util.stoppable import Stoppable, stoppable_method, stopping_method


class CallHandle(Stoppable):
    """A means to stopped a task."""

    def __init__(self, invoker, call_id):
        super(CallHandle, self).__init__()
        self._invoker = invoker
        self._call_id = call_id

    @stoppable_method
    @stopping_method
    def stop(self, reason=None):
        """
        Cancels the worker executing this call.

        Gets called by a timer from another thread.
        """
        if reason is None:
            reason = LayoffException("Stopping a call via its call handle.")
        self._invoker.stop_call(call_id=self._call_id, reason=reason)
