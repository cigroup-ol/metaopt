# -*- coding: utf-8 -*-
"""
Invoker that uses a single core or CPU respectively.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.call.call import call
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
            value = call(self.f, fargs)
            self._caller.on_result(value=value, fargs=fargs, **kwargs)
        except Exception as value:
            self._caller.on_error(value=value, fargs=fargs, **kwargs)

    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass
