# -*- coding: utf-8 -*-
"""
Plugin that logs the current optimum to standard output.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.plugin.plugin import Plugin


class OptimumPrintPlugin(Plugin):
    """
    Logs new optima for all return values to the standard output on result.

    For example::

        Minimum for value: f(a=0.1, b=0.2) = 0.7

    """
    def __init__(self):
        self._optima = dict()  # holds a tuple of args and result for each name

    def on_invoke(self, invocation):
        # There are no new optima in invokes, so do nothing.
        pass

    def on_result(self, invocation):
        """
        Logs new optima to the standard output.
        """
        for return_value in invocation.function.return_spec.return_values:
            name = return_value['name']

            if name not in self._optima.keys() or \
                    self._optima[name][1] > invocation.current_result:

                self._optima[name] = (tuple(invocation.fargs),
                                      invocation.current_result)

                print("%s for %s: f%s = %s" % \
                      ("Minimum" if return_value['minimize'] else "Maximum",
                       name,
                       self._optima[name][0], self._optima[name][1]))

    def on_error(self, invocation):
        # There are no new optima in errors, so do nothing.
        pass
