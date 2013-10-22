"""
TODO document me
"""

from orges.args import call

class SimpleInvoker():
    def __init__(self):
        self.caller = None

    @property
    def caller(self):
        """Gets the caller."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        self._caller = value

    def invoke(self, f, fargs, *vargs):
        return_value = call(f, fargs)
        self.caller.on_result(fargs, return_value, *vargs)

    def wait(self):
        pass
