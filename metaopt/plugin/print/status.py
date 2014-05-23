# -*- coding: utf-8 -*-
"""
Plugin that logs some events to standard output.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.plugin.plugin import Plugin


class StatusPrintPlugin(Plugin):
    """
    Logs all invocation events to the standard output.

    For example::

        Started f(a=0.1, b=0.2)
        Started f(a=0.2, b=0.3)
        Finished f(a=0.1, b=0.2) = 0.7
        Failed f(a=0.2, b=0.3)

    """
    def on_invoke(self, invocation):
        print("Started", "f%s" % (tuple(invocation.fargs), ))

    def on_result(self, invocation):
        print("Finished", "f%s = %s" % (tuple(invocation.fargs),
                                        invocation.current_result))

    def on_error(self, invocation):
        print("Failed", "f%s, %s" % \
              (tuple(invocation.fargs), "\n" +
               str(invocation.error.__class__.__name__) + ": " +
               str(invocation.error)))
