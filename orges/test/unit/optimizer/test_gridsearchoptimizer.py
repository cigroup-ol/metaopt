from orges.framework.paramspec import ParamSpec

from orges.optimizer.gridsearchoptimizer import GridSearchOptimizer
from orges.invoker.simpleinvoker import SimpleInvoker


def f(a, b):
    return -(a + b)

param_spec = ParamSpec()

param_spec.int("a").interval((1, 2))
param_spec.int("b").interval((1, 2))

def test_optimize_returns_result():
    invoker = SimpleInvoker()

    optimizer = GridSearchOptimizer(invoker)
    args, minimum = optimizer.optimize(f, param_spec)

    assert args[0].value == 2
    assert args[1].value == 2
    assert minimum == -4

if __name__ == '__main__':
    import nose
    nose.runmodule()