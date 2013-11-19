from __future__ import division, print_function, with_statement

from orges.plugins.base import BaseInvocationPlugin


class PassInvocationPlugin(BaseInvocationPlugin):
    """
    Invocation plug-in that does nothing for all hooks.
    """

    def before_invoke(self, invocation):
        pass

    def on_invoke(self, invocation):
        pass

    def on_result(self, invocation):
        pass

    def on_error(self, invocation):
        pass
