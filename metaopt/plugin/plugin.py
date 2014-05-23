# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.plugin.base import BasePlugin


class Plugin(BasePlugin):
    """
    Plugin that does nothing for all hooks.
    """

    def __init__(self):
        super(Plugin, self).__init__()

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
