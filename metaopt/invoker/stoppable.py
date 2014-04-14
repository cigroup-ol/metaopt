"""
Invoker that can be stopped.
"""
from __future__ import division, print_function, with_statement

from metaopt.core.call import call
from metaopt.invoker.base import BaseInvoker
from metaopt.util.stoppable import stoppable_method

# TODO make this thread-safe


class StoppableInvoker(BaseInvoker):
    """Invoker that can be stopped."""

    def __init__(self):
        super(StoppableInvoker, self).__init__()
        self._f = None

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, function):
        self._f = function

    @stoppable_method
    def invoke(self, caller, fargs, **kwargs):
        self._caller = caller
        del caller
        call(self.f, fargs, **kwargs)

    def wait(self):
        raise NotImplementedError()

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()
