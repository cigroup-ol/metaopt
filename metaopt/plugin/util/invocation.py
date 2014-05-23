# -*- coding: utf-8 -*-
"""
Utilities for plugin implementations.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


class Invocation(object):
    """
    This class provides an API for plugins (via properties).

    An object of this class always corresponds to (possibly multiple)
    invocations of the *same* objective functions with the *same* set of
    arguments. Most notably, it grants access to all parameters that were
    passed to  :meth:`metaopt.plugin.base.BasePlugin.before_invoke`.

    Certain properties of this object provide control over the actual objective
    function invocations. Generally, changes to properties only persist until
    the next call of  :meth:`metaopt.plugin.base.BasePlugin.before_invoke`
    where they are changed to their default values.

    Other properties provide information about the current invocation and their
    values will change whenever the object function is invoked again. These
    kind of properties are prefixed by `current_`. Some properties like
    :attr:`tries` hold information about all invocations.

    """
    def __init__(self):
        self._args = None
        self._current_task = None
        self._current_result = None
        self._function = None
        self._kwargs = None
        self._retry = False
        self._tries = 0
        self._error = None

    @property
    def current_task(self):
        """
        The task of the current invocation

        A task is in this context a TaskHandle.
        """
        return self._current_task

    @current_task.setter
    def current_task(self, task):
        self._current_task = task

    @property
    def current_result(self):
        """
        The result of the current invocation.

        This is always the result of the most recent invocation if any.
        """
        return self._current_result

    @current_result.setter
    def current_result(self, result):
        self._current_result = result

    @property
    def function(self):
        """The objective function that is invoked"""
        return self._function

    @function.setter
    def function(self, function):
        self._function = function

    @property
    def fargs(self):
        """The arguments the objective function is applied to."""
        return self._args

    @fargs.setter
    def fargs(self, fargs):
        self._args = fargs

    @property
    def kwargs(self):
        """ The additional arguments (if any) that were passed to
        :func:`metaopt.invoker.pluggable.PluggableInvoker.invoke`"""
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    @property
    def retry(self):
        """If set to True the objective function will be invoked again"""
        return self._retry

    @retry.setter
    def retry(self, retry):
        self._retry = retry

    @property
    def tries(self):
        """Counts how often the objective function was invoked"""
        return self._tries

    @tries.setter
    def tries(self, value):
        self._tries = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    def __repr__(self):
        return str({"fargs": self.fargs, "kwargs": self.kwargs})
