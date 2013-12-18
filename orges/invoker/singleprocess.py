"""
Invoker that uses a single core or CPU respectively.
"""
from __future__ import division, print_function, with_statement

from orges.args import call
from orges.invoker.base import BaseInvoker


class SingleProcessInvoker(BaseInvoker):
    """Invoker that does the work on its own."""

    def __init__(self):
        super(SingleProcessInvoker, self).__init__(self)
        self._caller = None

    @property
    def caller(self):
        """Gets the caller."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        self._caller = value

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        pass

    def invoke(self, function, fargs, **vargs):
        """Calls back to self._caller.on_result() for call(f, fargs)."""
        try:
            result = call(function, fargs)
            self._caller.on_result(result, fargs, vargs)
        except Exception as exception:
            self._caller.on_error(fargs, vargs, exception)

    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass

    def abort(self):
        raise NotImplementedError()
