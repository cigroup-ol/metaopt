"""This module provides a plugin-enabled invoker implementation"""

from __future__ import division, print_function, with_statement

from orges.invoker.base import BaseInvoker
from orges.plugins.util import Invocation
from orges.optimizer.base import BaseCaller


class PluggableInvoker(BaseInvoker, BaseCaller):
    """
    Invoker with hooks for calling plugins in various situations.
    """

    def __init__(self, invoker, plugins=[]):
        """
        :param plugins: List of plugins to be executed in various situations.
        """
        super(PluggableInvoker, self).__init__(self)

        self.invoker = invoker
        self.invoker.caller = self
        self._caller = None
        self.plugins = plugins

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

        for plugin in self.plugins:
            plugin.on_error(invocation)

        self.caller.on_error(fargs, **invocation.kwargs)

    def wait(self):
        return self.invoker.wait()

    def abort(self):
        self.invoker.abort()
