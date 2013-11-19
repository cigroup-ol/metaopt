from __future__ import division, print_function, with_statement

from orges.invoker.pluggable import InvocationPlugin


class PrintInvocationPlugin(InvocationPlugin):
    """
    Logs all interaction with the invoker to the standard output.
    """
    def on_invoke(self, invocation):
        print("Started", "f%s" % (tuple(invocation.fargs),))

    def on_result(self, invocation):
        result = invocation.current_result
        print("Finished", "f%s=%s" % (tuple(invocation.fargs), result))

    def on_error(self, invocation):
        print("Failed", "f%s" % (tuple(invocation.fargs),))