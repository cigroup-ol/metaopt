"""
Integration test for main.py.
"""
from __future__ import division, print_function, with_statement

import nose
from nose.tools import eq_

from metaopt.core import param
from metaopt.core.main import custom_optimize
from metaopt.core.returns import maximize
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.optimizer.gridsearch import GridSearchOptimizer


@maximize("y")
@param.int("x", interval=[0, 10])
def f(x):
    return x


def test_custom_optimize_maximize_gridsearch_multiprocess():
    invoker = MultiProcessInvoker()
    optimizer = GridSearchOptimizer()

    result = custom_optimize(f, invoker, optimizer=optimizer)
    assert result is not None
    eq_(result[0].value, 10)

if __name__ == '__main__':
    nose.runmodule()
