"""
TODO document me
"""
from __future__ import division, print_function, with_statement


from metaopt.core import param
from metaopt.core.args import ArgsCreator
from metaopt.invoker.dualthread import DualThreadInvoker
from metaopt.optimizer.gridsearch import GridSearchOptimizer


@param.int("a", interval=(1, 2))
@param.int("b", interval=(1, 2))
def f(a, b):
    return -(a + b)


def test_optimize_returns_result():
    optimizer = GridSearchOptimizer()

    invoker = DualThreadInvoker()
    invoker.f = f
    invoker.param_spec = f.param_spec
    invoker.return_spec = None

    ARGS = list(ArgsCreator(f.param_spec).product())[-1]

    args = optimizer.optimize(invoker=invoker, function=f,
                              param_spec=f.param_spec)

    for arg0, arg1 in zip(args, ARGS):
        assert arg0 == arg1

if __name__ == '__main__':
    import nose
    nose.runmodule()
