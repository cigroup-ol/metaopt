"""This module provides a plugin-enabled invoker implementation"""

from __future__ import division, print_function, with_statement

from orges.invoker.base import BaseInvoker
from orges.plugins.util import Invocation
from orges.optimizer.base import BaseCaller
from orges.util.stoppable import stopping_method, stoppable_method,\
    StoppedException


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
        self.plugins = plugins

    @property
    def f(self):
        return self.invoker.f

    @f.setter
    def f(self, value):
        self.invoker.f = value

    @property
    def param_spec(self):
        return self.invoker.param_spec

    @param_spec.setter
    def param_spec(self, value):
        self.invoker.param_spec = value

    @property
    def return_spec(self):
        return self.invoker.return_spec

    @return_spec.setter
    def return_spec(self, value):
        self.invoker.return_spec = value

    @property
    def invoker(self):
        """Property for the invoker attribute."""
        return self._invoker

    @stoppable_method
    def invoke(self, caller, fargs, invocation=None, **kwargs):
        """Implementation of the inherited abstract invoke method."""
        self.caller = caller

        if invocation is None:
            invocation = Invocation()

            invocation.function = self.f
            invocation.fargs = fargs
            invocation.kwargs = kwargs

        for plugin in self.plugins:
            plugin.before_invoke(invocation)

        invocation.tries += 1

        try:
            invocation.current_task = self.invoker.invoke(self, fargs, invocation=invocation)
        except StoppedException:
            return invocation.current_task

        for plugin in self.plugins:
            plugin.on_invoke(invocation)

        return invocation.current_task

    def on_result(self, result, fargs, invocation, **kwargs):
        """Implementation of the inherited abstract on_result method."""
        # TODO an invocation=None default makes no sense if the following fails
        invocation.current_result = result

        for plugin in self.plugins:
            plugin.on_result(invocation)

        if invocation.retry:
            # TODO: Maybe run this in its own thread
            self.invoke(self.caller, invocation.fargs, invocation, **invocation.kwargs)
        else:
            self.caller.on_result(result, fargs, **invocation.kwargs)

    def on_error(self, error, fargs, invocation):
        """Implementation of the inherited abstract on_error method."""
        for plugin in self.plugins:
            plugin.on_error(invocation)

        self.caller.on_error(error, fargs, **invocation.kwargs)

    def wait(self):
        """Implementation of the inherited abstract wait method."""
        return self.invoker.wait()

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this invoker."""
        self.invoker.stop()
