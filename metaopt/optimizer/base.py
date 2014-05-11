# -*- coding: utf-8 -*-
"""
This module provides an abstract base classes for implementing optimizers.

It provides two abstract base classes :class:`BaseOptimizer` and
:class:`BaseCaller`. All optimizers should implement :class:`BaseOptimizer`
and by that :class:`BaseCaller`. Objects that only call
:meth:`metaopt.invoker.base.BaseInvoker.invoke` and need to be called back by
the invoker but do not offer an :meth:`optimize`, may implement
:class:`BaseCaller`, only.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from abc import ABCMeta, abstractmethod


class BaseCaller(object):
    """Abstract base class for objects calling
    :meth:`metaopt.invoker.base.BaseInvoker.invoke` (who calls it back).
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        super(BaseCaller, self).__init__()

    @abstractmethod
    def on_result(self, value, fargs, **kwargs):
        """
        Called when :meth:`metaopt.invoker.base.BaseInvoker.invoke` was
        successful.

        :param result: Return value of the objective function
        :param fargs: Arguments the objective function was applied to
        """
        pass

    @abstractmethod
    def on_error(self, value, fargs, **kwargs):
        """
        Called when :meth:`metaopt.invoker.base.BaseInvoker.invoke` was *not*
        successful.

        :param error: Error that occured
        :param fargs: Arguments the objective function was applied to
        """
        pass


class BaseOptimizer(BaseCaller):
    """
    Abstract base class for objects optimizing objective functions.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def optimize(self, invoker, param_spec, return_spec):
        """
        Optimize objective function for a given parameters specification.

        Currently, implementations are expected to *minimize* the objective
        function. This may change in later versions by using `return_spec`.

        :param param_spec: Parameters specification for `function`
        :param return_spec: Return value specification for `function`
        :returns: Optimal arguments
        """
        pass
