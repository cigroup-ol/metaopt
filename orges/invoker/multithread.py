"""
Invoker that runs tasks in threads.
"""
from __future__ import division, print_function, with_statement

from threading import Lock, Thread

from orges.core.args import call
from orges.invoker.base import BaseInvoker
from orges.invoker.util.TaskHandle import TaskHandle


class MultiThreadInvoker(BaseInvoker):
    """Invoker that runs tasks in threads."""

    def __init__(self):
        super(MultiThreadInvoker, self).__init__(self)
        self.thread = None
        self.lock = Lock()

        self.current_task = None
        self.cancelled = False
        self.aborted = False

    @property
    def caller(self):
        return self._caller

    @caller.setter
    def caller(self, value):
        self._caller = value

    def get_subinvoker(self, resources):
        return self

    def invoke(self, f, fargs, **kwargs):
        with self.lock:
            if self.aborted:
                return None, True

        self.wait()

        with self.lock:
            self.task = TaskHandle(self)

        self.thread = Thread(target=self.target, args=(f, fargs),
                             kwargs=kwargs)
        self.thread.start()

        with self.lock:
            aborted = self.aborted

        return self.task, aborted

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
            self._caller.on_result(return_value, fargs, **kwargs)
        else:
            self._caller.on_error(fargs, **kwargs)

    def wait(self):
        if self.thread is not None:
            self.thread.join()

        with self.lock:
            aborted = self.aborted

        return aborted

    def abort(self):
        with self.lock:
            self.aborted = True

        self.cancel(self.current_task)
