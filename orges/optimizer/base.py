"""
This module provides an abstract base class for implementing optimizer
"""

from __future__ import division, print_function, with_statement

from abc import abstractmethod, ABCMeta  # Abstract Base Class


class BaseOptimizer(object):
    """
    Abstract base class for objects optimizing objective functions.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def optimize(self, function, param_spec, return_spec):
        """
        :param function: Objective function
        :param param_spec: Parameters specification for `function`
        :param return_spec: Return value specification for `function`
        """

    # TODO: Include invoker property

class BaseCaller(object):
    """Abstract base class for objects calling
    :meth:`orges.invoker.base.BaseInvoker.invoke` (and being called back by it).
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self._invoker = None

    @property
    @abstractmethod
    def invoker(self):
        "The invoker that is used by this caller."
        return self._invoker

    @invoker.setter
    @abstractmethod
    def invoker(self, invoker):
        self._invoker = invoker

    @abstractmethod
    def on_result(self, result, fargs, *vargs, **kwargs):
        """
        Called when :meth:`orges.invoker.base.BaseInvoker.invoke` was
        successful.

        :param result: Return value of the objective function
        :param fargs: Arguments the objective function was applied to
        """
        pass

    @abstractmethod
    def on_error(self, error, fargs, *vargs, **kwargs):
        """
        Called when :meth:`orges.invoker.base.BaseInvoker.invoke` was *not*
        successful.

        :param error: Error that occured
        :param fargs: Arguments the objective function was applied to
        """
        pass
