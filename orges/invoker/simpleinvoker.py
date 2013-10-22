"""
TODO document me
"""

from orges.args import call
from orges.invoker.invoker import Invoker


class SimpleInvoker(Invoker):
    """TODO document me"""

    def __init__(self, resources):
        self._caller = None
        self.resources = resources
        super(SimpleInvoker, self).__init__(self, resources)

    @property
    def caller(self):
        """Gets the caller."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        self._caller = value

    def get_subinvoker(self, resources):
        """TODO document me"""
        # TODO implement me
        pass

    def invoke(self, f, fargs, **vargs):
        return_value = call(f, fargs)
        self._caller.on_result(return_value, fargs, vargs)

    def wait(self):
        pass
