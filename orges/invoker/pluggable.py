"""This module provides a plugin-enabled invoker implementation"""

from __future__ import division, print_function, with_statement

from orges.invoker.base import BaseInvoker
from orges.plugins.util import Invocation
from orges.optimizer.base import BaseCaller


class PluggableInvoker(BaseInvoker, BaseCaller):
    """
    Invoker that uses other invokers and allows plugins to be used.
    """

    def __init__(self, invoker, plugins=[]):
        """
        :param invoker: Other invoker
        :param plugins: List of plugins
        """
        super(PluggableInvoker, self).__init__(self)

        # define self._invoker attribute and initialize it using property
        self._invoker = None
        self.invoker = invoker

        self.invoker.caller = self
        self._caller = None
        self.plugins = plugins

    @property
    def caller(self):
        """Property for the caller attribute."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Setter for the caller attribute."""
        self._caller = value

    @property
    def invoker(self):
        """Property for the invoker attribute."""
        return self._invoker

    @invoker.setter
    def invoker(self, invoker):
        """Setter for the invoker attribute."""
        invoker.caller = self
        self._invoker = invoker

    def get_subinvoker(self, resources):
        pass

    def invoke(self, function, fargs, invocation=None, **kwargs):
        """Implementation of the inherited abstract invoke method."""
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
        """Implementation of the inherited abstract on_result method."""
        if invocation is None:
            invocation = Invocation()
        invocation.current_result = result
        invocation.fargs = fargs
        invocation.vargs = vargs
        invocation.kwargs = kwargs

        for plugin in self.plugins:
            plugin.on_result(invocation)

        if invocation.retry:
            # TODO: Maybe run this in its own thread
            self.invoke(
                invocation.function,
                invocation.fargs,
                invocation,
                **invocation.kwargs)
        else:
            self.caller.on_result(fitness=result, args=fargs,
                                  *invocation.vargs)

    def on_error(self, fargs, invocation):
        """Implementation of the inherited abstract on_error method."""
        for plugin in self.plugins:
            plugin.on_error(invocation)

        self.caller.on_error(fargs, **invocation.kwargs)

    def wait(self):
        """Implementation of the inherited abstract wait method."""
        return self.invoker.wait()

    def abort(self):
        # TODO rename this to stop
        self.invoker.abort()
