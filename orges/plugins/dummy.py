from __future__ import division, print_function, with_statement

from orges.plugins.base import BasePlugin


class DummyPlugin(BasePlugin):
    """
    Invocation plugin that does nothing for all hooks.
    """

    def setup(self, f, param_spec, return_spec):
        """Do nothing"""
        pass

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
