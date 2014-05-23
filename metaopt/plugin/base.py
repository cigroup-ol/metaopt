# -*- coding: utf-8 -*-
"""
This module provides an abstract base class for invocation plugins.
"""


# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from abc import ABCMeta, abstractmethod


class BasePlugin(object):
    """
    Abstract base class for invocation plugins.

    Plugin developers can either derive their objects directly from this class
    or from :class:`metaopt.plugin.plugin.DummyPlugin` to only override
    methods selectively.

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        super(BasePlugin, self).__init__()

    @abstractmethod
    def setup(self, f, param_spec, return_spec):
        """
        Called before the invoker calls the objective function the first time

        :param f: Objective function
        :param param_spec: Parameter specification
        :param return_spec: Return value specification
        """
        pass

    @abstractmethod
    def before_invoke(self, invocation):
        """
        Called right before the invoker calls the objective function

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`metaopt.invoker.pluggable.Invocation`
        """
        pass

    @abstractmethod
    def on_invoke(self, invocation):
        """
        Called after the invoker called the objective function

        Since objective functions are usually called asynchronously `invocation`
        will not contain any results yet.

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`metaopt.invoker.pluggable.Invocation`
        """
        pass

    @abstractmethod
    def on_result(self, invocation):
        """
        Called when the invocation of the objective function was successful

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`metaopt.invoker.pluggable.Invocation`
        """
        pass

    @abstractmethod
    def on_error(self, invocation):
        """
        Called when the invocation of the objective function was not successful

        Since the invocation was not successful `invocation` will not contain
        any result.

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`metaopt.invoker.pluggable.Invocation`
        """
        pass
