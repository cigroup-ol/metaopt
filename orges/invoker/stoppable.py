"""
Invoker that can be stopped.
"""
from __future__ import division, print_function, with_statement

from orges.core.call import call
from orges.invoker.base import BaseInvoker
from orges.util.stoppable import stoppable_method

# TODO make this thread-safe


class StoppableInvoker(BaseInvoker):
    """Invoker that can be stopped."""

    def __init__(self):
        super(StoppableInvoker, self).__init__()

    @stoppable_method
    def invoke(self, caller, fargs, **kwargs):
        call(self.f, fargs, **kwargs)

    def wait(self):
        raise NotImplementedError()

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()
