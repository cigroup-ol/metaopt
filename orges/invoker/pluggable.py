from threading import Timer

from orges.invoker.base import Invoker, Caller

class PluggableInvoker(Invoker, Caller):
    def __init__(self, resources, invoker, plugins=[]):
        self.invoker = invoker
        self.invoker.caller = self

        self.plugins = plugins

    @property
    def caller(self):
        return self._caller

    @caller.setter
    def caller(self, value):
        self._caller = value

    def get_subinvoker(self, resources):
        pass

    def invoke(self, f, fargs, **kwargs):
        task = self.invoker.invoke(f, fargs, **kwargs)

        invocation = Invocation()
        invocation.current_task = task
        invocation.args = fargs

        for plugin in self.plugins:
            plugin.on_invoke(invocation)

        #print "Starting", "f%s" % (fargs,)

        # TODO: Implement this as plugin


    def on_result(self, return_value, fargs, **kwargs):
        # print "Finished", "f%s = %s" % (fargs, return_value)

        for plugin in self.plugins:
            plugin.on_result(None)  # TODO: Pass Invocation object

        self.caller.on_result(return_value, fargs, **kwargs)

    def on_error(self, fargs, **kwargs):
        # print "Failed", "f%s" % (fargs,)

        for plugin in self.plugins:
            plugin.on_error(None)  # TODO: Pass Invocation object

        self.caller.on_error(fargs, **kwargs)

    def wait(self):
        self.invoker.wait()

class Invocation():
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
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    def __repr__(self):
        return str(self.args)

class InvocationPlugin():
    def on_invoke(self, invocation):
        pass

    def on_result(self, invocation):
        pass

    def on_error(self, invocation):
        pass


class PrintInvocationPlugin(InvocationPlugin):
    def on_invoke(self, invocation):
        print "Started", invocation
        # print "Started", "f%s" % (fargs,)

    def on_result(self, invocation):
        print "Finished", invocation
        # print "Finished", "f%s = %s" % (fargs, return_value)

    def on_error(self, invocation):
        print "Failed", invocation
        # print "Failed", "f%s" % (fargs,)


class TimeoutInvocationPlugin(InvocationPlugin):
    def __init__(self, timeout):
        self.timeout = timeout

    def on_invoke(self, invocation):
        current_task = invocation.current_task
        Timer(self.timeout, current_task.cancel).start()