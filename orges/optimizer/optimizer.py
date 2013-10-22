"""
Abstract optimizer defining the API of optimizer implementations.
"""

import abc  # Abstract Base Class


class Optimizer(object):
    """Abstract invoker managing calls to ."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def optimize(self, f, param_spec, return_spec, minimize):
        """Handles a result."""
        pass

    @abc.abstractmethod
    def on_result(self, result, args, vargs):
        """Handles a result."""
        pass

    @abc.abstractmethod
    def on_error(self, error, args, vargs):
        """Handles an error."""
        pass
