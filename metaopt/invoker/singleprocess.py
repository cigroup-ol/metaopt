"""
Invoker that uses a single core or CPU respectively.
"""
from __future__ import division, print_function, with_statement

from metaopt.core.call import call
from metaopt.invoker.base import BaseInvoker
from metaopt.util.stoppable import stoppable_method, stopping_method


class SingleProcessInvoker(BaseInvoker):
    """Invoker that does the work on its own."""

    def __init__(self):
        super(SingleProcessInvoker, self).__init__()

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, f):
        self._f = f

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()

    @stoppable_method
    def invoke(self, caller, fargs, **kwargs):
        """Calls back to self._caller.on_result() for call(f, fargs)."""
        self._caller = caller
        del caller
        try:
            result = call(self.f, fargs)
            self._caller.on_result(result, fargs, **kwargs)
        except Exception as error:
            self._caller.on_error(error, fargs, **kwargs)

    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this invoker."""
        raise NotImplementedError()
