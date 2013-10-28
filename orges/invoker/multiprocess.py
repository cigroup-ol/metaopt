"""
Invoker that uses multiple cores or CPUs respectively.
"""
from orges.invoker.base import BaseInvoker
from orges.args import call


class MultiProcessInvoker(BaseInvoker):
    """Invoker that manages worker processes that do the actual work."""

    def __init__(self, resources):
        """
        resources - number of CPUs to use.
        """
        self._caller = None
        self.resources = resources
        super(MultiProcessInvoker, self).__init__(self, resources)

    @property
    def caller(self):
        """Gets the caller."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        self._caller = value

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amout of resources of self."""
        pass

    def invoke(self, f, fargs, **vargs):
        """Calls back to self._caller.on_result() for call(f, fargs)."""
        try:
            result = call(f, fargs)
        except Exception as exception:
            self._caller.on_error(exception, fargs, vargs)
            return
        self._caller.on_result(result, fargs, vargs)

    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass
