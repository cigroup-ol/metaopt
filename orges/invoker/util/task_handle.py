"""
Utilities for invokers.
"""
from __future__ import division, print_function, with_statement


class TaskHandle(object):
    """A means to stop a task."""

    def __init__(self, invoker, task_id):
        self._invoker = invoker
        self._task_id = task_id

    def stop(self):
        """Cancels this task."""
        self._invoker.stop(self._task_id)
