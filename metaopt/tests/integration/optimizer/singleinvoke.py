# -*- coding: utf-8 -*-
"""
Tests for the single invoke invoker.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from mock import Mock

# First Party
from metaopt.concurrent.invoker.singleprocess import SingleProcessInvoker
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.wrapper import ReturnValuesWrapper
from metaopt.optimizer.singleinvoke import SingleInvokeOptimizer


@param.int("a", interval=(2, 2))
@param.int("b", interval=(1, 1))
def f(a, b):
    return -(a + b)


def test_optimize_returns_result():
    optimizer = SingleInvokeOptimizer()
    optimizer.on_result = Mock()
    optimizer.on_error = Mock()

    invoker = SingleProcessInvoker()
    invoker.f = f

    optimizer.optimize(invoker=invoker, param_spec=f.param_spec,
                       return_spec=None)

    args = ArgsCreator(f.param_spec).args()

    assert not optimizer.on_error.called
    optimizer.on_result.assert_called_with(value=ReturnValuesWrapper(None, -3),
                                           fargs=args)

if __name__ == '__main__':
    nose.runmodule()
