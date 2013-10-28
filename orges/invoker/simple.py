"""
TODO document me
"""

from threading import Thread, Lock

from orges.args import call
from orges.invoker.base import BaseInvoker


class SimpleInvoker(BaseInvoker):
    """TODO document me"""

    def __init__(self, resources):
        super(SimpleInvoker, self).__init__(self, resources)
        self.thread = None
        self.lock = Lock()

        self.current_task = None
        self.cancelled = False

    @property
    def caller(self):
        return self._caller

    @caller.setter
    def caller(self, value):
        self._caller = value

    def get_subinvoker(self, resources):
        return self

    def invoke(self, f, fargs, **kwargs):
        self.wait()

        with self.lock:
            self.task = Task(self)

        self.thread = Thread(target=self.target, args=(f, fargs), kwargs=kwargs)
        self.thread.start()

        return self.task

    def cancel(self, task):
        with self.lock:
            if self.task is not task:
                return

        with self.lock:
            self.cancelled = True

    def target(self, f, fargs, **kwargs):
        return_value = call(f, fargs)

        with self.lock:
            cancelled = self.cancelled
            self.cancelled = False

        if not cancelled:
            self.caller.on_result(return_value, fargs, **kwargs)
        else:
            self.caller.on_error(fargs, **kwargs)

    def wait(self):
        if self.thread is not None:
            self.thread.join()

class Task(object):
    def __init__(self, simple_invoker):
        self.simple_invoker = simple_invoker

    def cancel(self):
        self.simple_invoker.cancel(self)
