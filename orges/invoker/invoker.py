"""
Abstract invoker defining the API of invoker implementations.
"""

import abc  # Abstract Base Class


class Invoker(object):
    """Abstract invoker managing calls to ."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, resources, caller):
        pass

    @abc.abstractmethod
    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amout of resources of self."""
        pass

    @abc.abstractmethod
    def invoke(self, f, args, **vargs):
        """Calls back to self.caller.on_result() for call(f, args)."""
        # try:
        #     ret = call(f, args)
        # except Exception as exception:
        #     caller.on_error(args, vargs, exception)
        #     return
        # caller.on_result(args, vargs)
        pass

    @abc.abstractmethod
    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass
