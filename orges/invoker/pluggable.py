from __future__ import division, print_function, with_statement

from orges.invoker.base import BaseInvoker
from orges.optimizer.base import BaseCaller


class PluggableInvoker(BaseInvoker, BaseCaller):
    """
    Invoker with hooks for calling plug-ins in various situations.
    """

    def __init__(self, resources, invoker, plugins=[]):
        """
        :param plugins: List of plug-ins to be executed in various situations.
        """
        self.invoker = invoker
        self.invoker.caller = self
        self._caller = None
        self.plugins = plugins

        print(resources)

        super(PluggableInvoker, self).__init__(self, invoker)

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

            invocation.f_package = function
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
                invocation.f_package,
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
    TODO document me
    """
    def __init__(self):
        self._retry = False
        self._tries = 0

    @property
    def current_task(self):
        return self._current_task

    @current_task.setter
    def current_task(self, task):
        self._current_task = task

    @property
    def current_result(self):
        return self._current_result

    @current_result.setter
    def current_result(self, result):
        self._current_result = result

    @property
    def f_package(self):
        return self._f_package

    @f_package.setter
    def f_package(self, f_package):
        self._f_package = f_package

    @property
    def fargs(self):
        return self._args

    @fargs.setter
    def fargs(self, fargs):
        self._args = fargs

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs

    @property
    def retry(self):
        return self._retry

    @retry.setter
    def retry(self, retry):
        self._retry = retry

    @property
    def tries(self):
        return self._tries

    @tries.setter
    def tries(self, value):
        self._tries = value

    def __repr__(self):
        return str(self.fargs)


class InvocationPlugin(object):
    """
    Base class for invocation plug-ins.
    """

    def before_invoke(self, invocation):
        """
        Gets called when plugpable invoker starts preparing a calls to invoke.
        """
        pass

    def on_invoke(self, invocation):
        """
        Gets called right before pluggable invoker calls invoke on its invoker.
        """
        pass

    def on_result(self, invocation):
        """
        Gets called when pluggable invoker receives a callback to on_result.
        """
        pass

    def on_error(self, invocation):
        """
        Gets called when pluggable invoker receives a callback to on_error.
        """
        pass
