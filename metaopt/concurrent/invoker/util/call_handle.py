# -*- coding: utf-8 -*-
"""
Means to stop tasks for invokers.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.concurrent.employer.util.exception import LayoffError
from metaopt.core.stoppable.stoppable import Stoppable
from metaopt.core.stoppable.util.decorator import stoppable, stopping
from metaopt.core.stoppable.util.exception import StoppedError


class CallHandle(Stoppable):
    """A means to stopped a task."""

    def __init__(self, invoker, call_id):
        super(CallHandle, self).__init__()

        self._invoker = invoker
        self._call_id = call_id

    @stoppable
    @stopping
    def stop(self, reason=None):
        """
        Cancels the worker executing this call.

        Gets called by a timer from another thread.
        """
        if reason is None:
            reason = LayoffError("Stopping a call via its call handle.")

        try:
            self._invoker.stop_call(call_id=self._call_id, reason=reason)
        except StoppedError:
            # The invoker was already stopped.
            # So there is nothing left to do here
            pass
