# -*- coding: utf-8 -*-
"""
Tests for the main module.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from mock import Mock

# First Party
from metaopt.core.optimize.optimize import custom_optimize


class TestCustomOptimize(object):

    def test_custom_optimize_stops_invoker(self):
        invoker = Mock()
        invoker.stop = Mock()

        optimizer = Mock()
        optimizer.optimize = Mock()
        optimizer.optimize.return_value = (1, 0)

        param_spec = Mock()
        return_spec = Mock()

        def f(x, y):
            pass

        custom_optimize(f, invoker, optimizer=optimizer, param_spec=param_spec,
            return_spec=return_spec)

        assert invoker.stop.called


if __name__ == '__main__':
    nose.runmodule()
