"""
Plugin that logs some events to standard output.
"""
from __future__ import division, print_function, with_statement

from metaopt.plugins.dummy import DummyPlugin


class PrintPlugin(DummyPlugin):
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
        print("Failed", "f%s, %s" % (tuple(invocation.fargs), "\n" +
            str(invocation.error.__class__.__name__) + ": " +
            str(invocation.error)))
