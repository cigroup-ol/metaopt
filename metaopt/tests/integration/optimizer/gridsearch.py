# -*- coding: utf-8 -*-
"""
TODO document me
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose

# First Party
from metaopt.concurrent.invoker.dualthread import DualThreadInvoker
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.paramspec.util import param
from metaopt.optimizer.gridsearch import GridSearchOptimizer


@param.int("a", interval=(1, 2))
@param.int("b", interval=(1, 2))
def f(a, b):
    return -(a + b)


class TestGridsearchOptimizer(object):
    def test_optimize_returns_result(self):
        optimizer = GridSearchOptimizer()

        invoker = DualThreadInvoker()
        invoker.f = f
        invoker.param_spec = f.param_spec
        invoker.return_spec = None

        ARGS = list(ArgsCreator(f.param_spec).product())[-1]

        args = optimizer.optimize(invoker=invoker, param_spec=f.param_spec)

        for arg0, arg1 in zip(args, ARGS):
            assert arg0 == arg1

if __name__ == '__main__':
    nose.runmodule()
