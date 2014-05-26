# -*- coding: utf-8 -*-
"""This module provides a plugin-enabled invoker implementation"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.concurrent.invoker.base import BaseInvoker
from metaopt.core.stoppable.util.decorator import stoppable, stopping
from metaopt.core.stoppable.util.exception import StoppedError
from metaopt.optimizer.base import BaseCaller
from metaopt.plugin.util.invocation import Invocation


class PluggableInvoker(BaseInvoker, BaseCaller):
    """
    Invoker that uses other invokers and allows plugins to be used.
    """

    def __init__(self, invoker, plugins=[]):
        """
        :param invoker: Other invoker
        :param plugins: List of plugins
        """
        super(PluggableInvoker, self).__init__()

        self._invoker = invoker
        self._plugins = plugins

        self._caller = None

    @property
    def f(self):
        return self._invoker.f

    @f.setter
    def f(self, function):
        self._invoker.f = function

    @property
    def param_spec(self):
        return self._invoker.param_spec

    @param_spec.setter
    def param_spec(self, param_spec):
        self._invoker.param_spec = param_spec

    @property
    def return_spec(self):
        return self._invoker.return_spec

    @return_spec.setter
    def return_spec(self, return_spec):
        self._invoker.return_spec = return_spec

    @property
    def invoker(self):
        """Property for the invoker attribute."""
        return self._invoker

    @stoppable
    def invoke(self, caller, fargs, invocation=None, **kwargs):
        """Implementation of the inherited abstract invoke method."""
        self._caller = caller

        if invocation is None:
            invocation = Invocation()

            invocation.function = self.f
            invocation.fargs = fargs
            invocation.kwargs = kwargs

            for plugin in self._plugins:
                plugin.setup(self.f, self.param_spec, self.return_spec)

        for plugin in self._plugins:
            plugin.before_invoke(invocation)

        invocation.tries += 1

        try:
            invocation.current_task = \
                self._invoker.invoke(caller=self, fargs=fargs,
                                     invocation=invocation)
        except StoppedError:
            return invocation.current_task

        # FIXME: This should not be required somehow
        if not invocation.current_task:
            return

        for plugin in self._plugins:
            plugin.on_invoke(invocation)

        return invocation.current_task

    def on_result(self, value, fargs, invocation, **kwargs):
        """Implementation of the inherited abstract on_result method."""
        del kwargs
        # TODO an invocation=None default makes no sense if the following fails
        invocation.current_result = value

        for plugin in self._plugins:
            plugin.on_result(invocation)

        if invocation.retry:
            # TODO: Maybe run this in its own thread
            self.invoke(caller=self._caller, fargs=invocation.fargs,
                        invocation=invocation, **invocation.kwargs)
        else:
            self._caller.on_result(value=value, fargs=fargs,
                                   invocation=invocation, **invocation.kwargs)

    def on_error(self, value, fargs, invocation, **kwargs):
        """Implementation of the inherited abstract on_error method."""
        del kwargs
        invocation.error = value

        for plugin in self._plugins:
            plugin.on_error(invocation=invocation)

        self._caller.on_error(value=value, fargs=fargs, invocation=invocation,
                              **invocation.kwargs)

        invocation.error = None

    def wait(self):
        """Implementation of the inherited abstract wait method."""
        return self._invoker.wait()

    @stoppable
    @stopping
    def stop(self, reason=None):
        """Stops this invoker."""
        try:
            self._invoker.stop(reason=reason)
        except StoppedError:
            pass
