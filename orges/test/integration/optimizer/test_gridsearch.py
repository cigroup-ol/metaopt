"""
TODO document me
"""
from __future__ import division, print_function, with_statement

from orges import param
from orges.args import ArgsCreator
from orges.invoker.simple import SimpleInvoker
from orges.optimizer.gridsearch import GridSearchOptimizer


@param.int("a", interval=(1, 2))
@param.int("b", interval=(1, 2))
def f(a, b):
    return -(a + b)

ARGS = list(ArgsCreator(f.param_spec).product())[-1]


def test_optimize_returns_result():
    invoker = SimpleInvoker()
    optimizer = GridSearchOptimizer()
    optimizer.invoker = invoker

    args = optimizer.optimize(f, f.param_spec)
    assert map(lambda arg: arg.value, args) == map(lambda arg: arg.value, ARGS)

if __name__ == '__main__':
    import nose
    nose.runmodule()
