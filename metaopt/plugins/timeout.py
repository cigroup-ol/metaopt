# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from threading import Timer

# First Party
from metaopt.plugins.plugin import Plugin


class TimeoutPlugin(Plugin):
    """
    Abort an invocation after a certain amount of time.

    Use this plugin for objective functions that may take too long to compute a
    result for certain parameters.

    """
    def __init__(self, timeout):
        """
        :param timeout: Available time for invocation (in seconds)
        """
        super(TimeoutPlugin, self).__init__()

        self.timeout = timeout

    def on_invoke(self, invocation):
        current_task = invocation.current_task

        def stop_task():
            error = TimeoutError(
                "The objective function took longer than %s seconds"\
                % self.timeout
            )

            current_task.stop(error)

        Timer(self.timeout, stop_task).start()

class TimeoutError(Exception):
    pass