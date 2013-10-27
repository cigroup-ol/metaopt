from threading import Timer

from orges.invoker.base import Invoker, Caller

class PluggableInvoker(Invoker, Caller):
    def __init__(self, resources, invoker):
        self.invoker = invoker
        self.invoker.caller = self

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

        print "Starting", "f%s" % (fargs,)

        # TODO: Implement this as plugin
        timer = Timer(1, task.cancel) # Cancel after 1 second
        timer.start()

    def on_result(self, return_value, fargs, **kwargs):
        print "Finished", "f%s = %s" % (fargs, return_value)
        self.caller.on_result(return_value, fargs, **kwargs)

    def on_error(self, fargs, **kwargs):
        print "Failed", "f%s" % (fargs,)
        self.caller.on_error(fargs, **kwargs)

    def wait(self):
        self.invoker.wait()

class Invocation():
    pass

class InvocationPlugin():
    pass