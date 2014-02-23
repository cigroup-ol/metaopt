"""
Integration test for main.py.
"""

from __future__ import division, print_function, with_statement

from time import sleep

from nose.tools import eq_

from metaopt.core import param
from metaopt.core.main import custom_optimize
from metaopt.core.returns import maximize, minimize
from metaopt.invoker.dualthread import DualThreadInvoker
from metaopt.optimizer.gridsearch import GridSearchOptimizer


def test_custom_optimize_maximize_gridsearch_dualthread():
    invoker = DualThreadInvoker()
    optimizer = GridSearchOptimizer()

    @maximize("y")
    @param.int("x", interval=[0, 10])
    def f(x):
        return x

    result = custom_optimize(f, invoker, optimizer=optimizer)
    eq_(result[0].value, 10)

def test_custom_optimize_minimize_gridsearch_dualthread():
    invoker = DualThreadInvoker()
    optimizer = GridSearchOptimizer()

    @minimize("y")
    @param.int("x", interval=[0, 10])
    def f(x):
        return x

    result = custom_optimize(f, invoker, optimizer=optimizer)
    eq_(result[0].value, 0)

def test_custom_optimize_maximize_gridsearch_dualthread_global_timeout():
    invoker = DualThreadInvoker()
    optimizer = GridSearchOptimizer()

    @maximize("y")
    @param.int("x", interval=[0, 10])
    def f(x):
        sleep(1)
        return x

    result = custom_optimize(f, invoker, timeout=1, optimizer=optimizer)
    assert result[0].value < 10

if __name__ == '__main__':
    import nose
    nose.runmodule()
