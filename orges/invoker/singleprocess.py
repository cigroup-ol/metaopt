"""
Invoker that uses multiple cores or CPUs respectively.
"""
from orges.invoker.invoker import Invoker
from orges.args import call


class SingleProcessInvoker(Invoker):
    """Invoker that does the work on its own."""

    def __init__(self, resources):
        """
        resources - number of CPUs to use.
        """
        self.resources = resources
        self.resources = 1  # enforce
        self._caller = None
        super(SingleProcessInvoker, self).__init__(self, resources)

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
            self._caller.on_error(fargs, vargs, exception)
            return
        self._caller.on_result(result, fargs, vargs)

    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass
