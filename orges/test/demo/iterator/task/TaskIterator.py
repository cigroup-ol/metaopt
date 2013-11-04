"""
Wraps an ArgumentsIterator to return task objects.
"""
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from orges.invoker.multiprocess_lib.Worker import Task


class TaskIterator(object):
    """Wraps an ArgumentsIterator to return task objects."""

    def __init__(self, get_argument_batches):
        self.get_argument_batches = get_argument_batches

    def __iter__(self):
        return self

    def next(self):
        """Returns the next argument batch as a task."""
        try:
            argument_batch = next(self.get_argument_batches)
            return Task(argument_batch)
        except StopIteration:
            return Task("DONE")
