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
        caller - calling class's self
        """
        self.resources = resources
        self.resources = 1  # enforce
        super(SingleProcessInvoker, self).__init__(resources, self)

    @property
    def caller(self):
        """Gets the caller."""
        return self.caller

    @caller.setter
    def set_caller(self, caller):
        """Sets the caller."""
        self.caller = caller

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amout of resources of self."""
        pass

    def invoke(self, f, args, **vargs):
        """Calls back to self.caller.on_result() for call(f, args)."""
        try:
            result = call(f, args)
        except Exception as exception:
            self.caller.on_error(args, vargs, exception)
            return
        self.caller.on_result(args, vargs, result)

    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass
