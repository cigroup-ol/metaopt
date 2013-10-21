from orges.framework.args import call

class SimpleInvoker():
    def __init__(self):
        self.caller = None

    @property
    def caller(self):
        return self._caller

    @caller.setter
    def caller(self, value):
        self._caller = value

    def invoke(self, f, fargs, *vargs):
        return_value = call(f, fargs)
        self.caller.on_result(fargs, return_value, *vargs)

    def wait(self):
        pass