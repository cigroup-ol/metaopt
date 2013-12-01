"""
Abstract optimizer defining the API of optimizer implementations.
"""
from __future__ import division, print_function, with_statement

from abc import abstractmethod, ABCMeta  # Abstract Base Class


class BaseOptimizer(object):
    """
    Abstract optimizer, a systematic way to call a function with arguments.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def optimize(self, function, param_spec, return_spec):
        """
        :param function:
        :param param_spec: Parameter specification for the given function.
        :param return_spec: Return value specification for the given function.
        """


class BaseCaller(object):
    """Abstract caller handling calls to a given invoker."""

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
    def on_result(self, result, fargs, *vargs, **kwargs):
        '''
        Handles a result.

        :param return_value: Return value of the given arguments.
        :param fargs: The arguments given to a function.
        '''
        pass

    @abstractmethod
    def on_error(self, error, fargs, *vargs, **kwargs):
        '''
        Handles an error.

        :param fargs: The arguments given to a function.
        '''
        pass
