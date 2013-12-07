from __future__ import division, print_function, with_statement

from orges.plugins.base import BasePlugin


class DummyPlugin(BasePlugin):
    """
    Invocation plug-in that does nothing for all hooks.
    """

    def before_invoke(self, invocation):
        """Do nothing"""
        pass

    def on_invoke(self, invocation):
        """Do nothing"""
        pass

    def on_result(self, invocation):
        """Do nothing"""
        pass

    def on_error(self, invocation):
        """Do nothing"""
        pass
