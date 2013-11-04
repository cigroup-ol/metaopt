from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from threading import Timer

from orges.invoker.base import BaseInvoker, BaseCaller


class PluggableInvoker(BaseInvoker, BaseCaller):
    def __init__(self, resources, invoker, plugins=[]):
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

    def get_subinvoker(self, resources):
        pass

    def invoke(self, f, fargs, invocation=None, **kwargs):
        # TODO: Reuse existing invocation object
        if invocation is None:
            invocation = Invocation()

            invocation.f = f
            invocation.fargs = fargs
            invocation.kwargs = kwargs

        for plugin in self.plugins:
            plugin.before_invoke(invocation)

        invocation.tries += 1

        task, aborted = self.invoker.invoke(f, fargs, invocation=invocation)

        if aborted:
            return task, aborted

        invocation.current_task = task

        for plugin in self.plugins:
            plugin.on_invoke(invocation)

        return task, aborted

    def on_result(self, result, fargs, invocation):
        invocation.current_result = result

        for plugin in self.plugins:
            plugin.on_result(invocation)

        if invocation.retry:
            # TODO: Maybe run this in its own thread
            self.invoke(
                invocation.f,
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


class Invocation():
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
    def f(self):
        return self._f

    @f.setter
    def f(self, f):
        self._f = f

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


class InvocationPlugin():
    def before_invoke(self, invocation):
        pass

    def on_invoke(self, invocation):
        pass

    def on_result(self, invocation):
        pass

    def on_error(self, invocation):
        pass


class PrintInvocationPlugin(InvocationPlugin):
    def on_invoke(self, invocation):
        print("Started", "f%s" % (invocation.fargs,))

    def on_result(self, invocation):
        result = invocation.current_result
        print("Finished", "f%s=%s" % (invocation.fargs, result))

    def on_error(self, invocation):
        print("Failed", "f%s" % (invocation.fargs,))


class TimeoutInvocationPlugin(InvocationPlugin):
    def __init__(self, timeout):
        self.timeout = timeout

    def on_invoke(self, invocation):
        current_task = invocation.current_task
        Timer(self.timeout, current_task.cancel).start()
