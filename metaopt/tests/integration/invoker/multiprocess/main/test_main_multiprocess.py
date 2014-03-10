"""
Integration test for main.py.
"""
from __future__ import division, print_function, with_statement

from time import sleep

import nose

from metaopt.core import param
from metaopt.core.main import custom_optimize
from metaopt.core.returns import maximize
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.optimizer.gridsearch import GridSearchOptimizer


@maximize("y")
@param.int("x", interval=[0, 10])
def f(x):
    sleep(1)
    return x


def test_custom_optimize_maximize_gridsearch_multiprocess_global_timeout():
    invoker = MultiProcessInvoker()
    optimizer = GridSearchOptimizer()

    result = custom_optimize(f, invoker, timeout=1, optimizer=optimizer)
    assert result[0].value <= 10

if __name__ == '__main__':
    nose.runmodule()
