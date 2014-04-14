"""This module provides a plugin-enabled invoker implementation"""

from __future__ import division, print_function, with_statement

from metaopt.invoker.base import BaseInvoker
from metaopt.optimizer.base import BaseCaller
from metaopt.plugins.util import Invocation
from metaopt.util.stoppable import StoppedException, stoppable_method, \
    stopping_method


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
        self._caller = caller

        if invocation is None:
            invocation = Invocation()

            invocation.function = self.f
            invocation.fargs = fargs
            invocation.kwargs = kwargs

            for plugin in self.plugins:
                plugin.setup(self.f, self.param_spec, self.return_spec)

        for plugin in self.plugins:
            plugin.before_invoke(invocation)

        invocation.tries += 1

        try:
            invocation.current_task = self.invoker.invoke(caller=self, fargs=fargs,
                invocation=invocation)
        except StoppedException:
            return invocation.current_task

        # FIXME: This should not be required somehow
        if not invocation.current_task:
            return

        for plugin in self.plugins:
            plugin.on_invoke(invocation)

        return invocation.current_task

    def on_result(self, value, fargs, invocation, **kwargs):
        """Implementation of the inherited abstract on_result method."""
        # TODO an invocation=None default makes no sense if the following fails
        result = value
        invocation.current_result = result

        for plugin in self.plugins:
            plugin.on_result(invocation)

        if invocation.retry:
            # TODO: Maybe run this in its own thread
            self.invoke(self._caller, invocation.fargs, invocation,
                        **invocation.kwargs)
        else:
            self._caller.on_result(value=result, fargs=fargs, **invocation.kwargs)

    def on_error(self, error, fargs, invocation, **kwargs):
        """Implementation of the inherited abstract on_error method."""
        invocation.error = error

        for plugin in self.plugins:
            plugin.on_error(invocation)

        self._caller.on_error(error=error, fargs=fargs, **invocation.kwargs)

        invocation.error = None

    def wait(self):
        """Implementation of the inherited abstract wait method."""
        return self.invoker.wait()

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this invoker."""
        self.invoker.stop()
