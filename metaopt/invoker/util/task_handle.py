"""
Means to stop tasks for invokers.
"""
from __future__ import division, print_function, with_statement

from metaopt.util.stoppable import Stoppable, stoppable_method, stopping_method


class TaskHandle(Stoppable):
    """A means to stopped a task."""

    def __init__(self, invoker, task_id):
        self._invoker = invoker
        self._task_id = task_id
        super(TaskHandle, self).__init__()

    @stoppable_method
    @stopping_method
    def stop(self):
        """Cancels the worker executing this task."""
        self._invoker.stop_task(task_id=self._task_id)
