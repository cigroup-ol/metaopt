"""
Invoker that uses a single core or CPU respectively.
"""
from __future__ import division, print_function, with_statement

from metaopt.core.call import call
from metaopt.invoker.invoker import Invoker
from metaopt.util.stoppable import stoppable_method, stopping_method


class SingleProcessInvoker(Invoker):
    """Invoker that does the work on its own."""

    def __init__(self):
        super(SingleProcessInvoker, self).__init__()

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
