"""
Plugin that displays messages for all hooks.
"""

from __future__ import division, print_function, with_statement

from metaopt.plugins.plugin import Plugin


class DebugPlugin(Plugin):
    """
    Logs all interaction with the invoker to the standard output.
    """
    def before_invoke(self, invocation):
        print("Starting", "f%s" % (tuple(invocation.fargs), ))

    def on_invoke(self, invocation):
        print("Started", "f%s" % (tuple(invocation.fargs), ))

    def on_result(self, invocation):
        print("Finished", "f%s = %s" % (tuple(invocation.fargs),
                                        invocation.current_result))

    def on_error(self, invocation):
        print("Failed", "f%s" % (tuple(invocation.fargs)))
