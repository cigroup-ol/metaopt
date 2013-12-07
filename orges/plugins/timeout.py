from __future__ import division, print_function, with_statement

from threading import Timer

from orges.plugins.dummy import DummyPlugin


class TimeoutPlugin(DummyPlugin):
    """
    Sets a timeout for each call to invoke.
    """
    def __init__(self, timeout):
        self.timeout = timeout

    def on_invoke(self, invocation):
        current_task = invocation.current_task
        Timer(self.timeout, current_task.cancel).start()
