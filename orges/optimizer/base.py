"""
Abstract optimizer defining the API of optimizer implementations.
"""
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from abc import abstractmethod, ABCMeta  # Abstract Base Class


class BaseOptimizer(object):
    """Abstract _invoker managing calls to ."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self._invoker = None

    @property
    @abstractmethod
    def invoker(self):
        return self._invoker

    @invoker.setter
    @abstractmethod
    def invoker(self, invoker):
        self._invoker = invoker

    @abstractmethod
    def optimize(self, F_PACKAGE, param_spec, return_spec, minimize):
        """Handles a result."""
        pass

    @abstractmethod
    def on_result(self, result, args, vargs):
        """Handles a result."""
        pass

    @abstractmethod
    def on_error(self, error, args, vargs):
        """Handles an error."""
        pass
