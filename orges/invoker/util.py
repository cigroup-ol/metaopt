"""
Utilities for invokers.
"""


class TaskHandle(object):
    """A means to cancel a task."""

    def __init__(self, invoker, task_id):
        self._invoker = invoker
        self._task_id = task_id

    def cancel(self):
        """Cancels this task."""
        self._invoker.cancel(self._task_id)
