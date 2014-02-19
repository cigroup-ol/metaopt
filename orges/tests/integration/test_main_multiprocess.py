"""
Integration test for main.py.
"""

from __future__ import division, print_function, with_statement

from time import sleep

from nose.tools import eq_

from orges.core import param
from orges.core.main import custom_optimize
from orges.core.returns import maximize, minimize
from orges.invoker.multiprocess import MultiProcessInvoker
from orges.optimizer.gridsearch import GridSearchOptimizer


@maximize("y")
@param.int("x", interval=[0, 10])
def f(x):
    return x

def test_custom_optimize_maximize_gridsearch_multiprocess():
    invoker = MultiProcessInvoker()
    optimizer = GridSearchOptimizer()

    result = custom_optimize(f, invoker, optimizer=optimizer)
    eq_(result[0].value, 10)

@minimize("y")
@param.int("x", interval=[0, 10])
def f(x):
    return x

def test_custom_optimize_minimize_gridsearch_multiprocess():
    invoker = MultiProcessInvoker()
    optimizer = GridSearchOptimizer()

    result = custom_optimize(f, invoker, optimizer=optimizer)
    eq_(result[0].value, 0)

@maximize("y")
@param.int("x", interval=[0, 10])
def f(x):
    sleep(1)
    return x

def test_custom_optimize_maximize_gridsearch_multiprocess_global_timeout():
    invoker = MultiProcessInvoker()
    optimizer = GridSearchOptimizer()

    result = custom_optimize(f, invoker, timeout=1, optimizer=optimizer)
    assert result[0].value < 10

if __name__ == '__main__':
    import nose
    nose.runmodule()
