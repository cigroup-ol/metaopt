"""This module provides a plugin-enabled invoker implementation"""

from __future__ import division, print_function, with_statement

from orges.invoker.base import BaseInvoker
from orges.optimizer.base import BaseCaller


class PluggableInvoker(BaseInvoker, BaseCaller):
    """
    Invoker with hooks for calling plug-ins in various situations.
    """

    def __init__(self, invoker, plugins=[]):
        """
        :param plugins: List of plug-ins to be executed in various situations.
        """
        self.invoker = invoker
        self.invoker.caller = self
        self._caller = None
        self.plugins = plugins

        super(PluggableInvoker, self).__init__(self)

    @property
    def caller(self):
        return self._caller

    @caller.setter
    def caller(self, value):
        self._caller = value

    @property
    def invoker(self):
        return self._invoker

    @invoker.setter
    def invoker(self, invoker):
        invoker.caller = self
        self._invoker = invoker

    def get_subinvoker(self, resources):
        pass

    def invoke(self, function, fargs, invocation=None, **kwargs):
        # TODO: Reuse existing invocation object
        if invocation is None:
            invocation = Invocation()

            invocation.function = function
            invocation.fargs = fargs
            invocation.kwargs = kwargs

        for plugin in self.plugins:
            plugin.before_invoke(invocation)

        invocation.tries += 1

        task, aborted = self.invoker.invoke(function, fargs,
                                            invocation=invocation)

        if aborted:
            return task, aborted

        invocation.current_task = task

        for plugin in self.plugins:
            plugin.on_invoke(invocation)

        return task, aborted

    def on_result(self, result, fargs, invocation=None, *vargs, **kwargs):
        del vargs
        del kwargs

        invocation.current_result = result

        for plugin in self.plugins:
            plugin.on_result(invocation)

        if invocation.retry:
            # TODO: Maybe run this in its own thread
            self.invoke(
                invocation.function,
                invocation.fargs,
                invocation,
                **invocation.kwargs
            )
        else:
            self.caller.on_result(result, fargs, **invocation.kwargs)

    def on_error(self, fargs, invocation):

        for plugin in self.plugins:
            plugin.on_error(invocation)

        self.caller.on_error(fargs, **invocation.kwargs)

    def wait(self):
        return self.invoker.wait()

    def abort(self):
        self.invoker.abort()


class Invocation(object):
    """
    This class provides an API for plugins (via properties).

    An object of this class always corresponds to (possibly multiple)
    invocations of the *same* objective functions with the *same* set of
    arguments. Most notably, it grants access to all parameters that were passed
    to  :meth:`orges.plugins.base.BasePlugin.before_invoke`.

    Certain properties of this object provide control over the actual objective
    function invocations. Generally, changes to properties only persist until
    the next call of  :meth:`orges.plugins.base.BasePlugin.before_invoke` where
    they are changed to their default values.

    Other properties provide information about the current invocation and their
    values will change whenever the object function is invoked again. These kind
    of properties are prefixed by `current_`. Some properties like :attr:`tries`
    hold information about all invocations.

    """
    def __init__(self):
        # TODO: Initialize all properties to default value
        self._retry = False
        self._tries = 0

    @property
    def current_task(self):
        """
        The task of the current invocation

        TODO: Document what exactly a task is

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
        :func:`orges.invoker.pluggable.PluggableInvoker.invoke`"""
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

    def __repr__(self):
        return str(self.fargs)
