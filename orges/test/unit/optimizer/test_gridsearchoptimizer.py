"""
TODO document me
"""

from orges.optimizer.gridsearchoptimizer import GridSearchOptimizer
from orges.paramspec import ParamSpec
from orges.invoker.simpleinvoker import SimpleInvoker
from orges.invoker.multiprocess import MultiProcessInvoker
from orges.invoker.singleprocess import SingleProcessInvoker


def f(a, b):
    return -(a + b)

PARAM_SPEC = ParamSpec()
PARAM_SPEC.int("a", interval=(1, 2))
PARAM_SPEC.int("b", interval=(1, 2))


class Caller(object):

    def __init__(self):
        pass

    def on_result(self, args, vargs, result):
        pass


def test_optimize_returns_result():
    resources = 2  # should get ignored
    invoker = SimpleInvoker(resources)
    invoker.caller = Caller()
    optimizer = GridSearchOptimizer(invoker)
    args, minimum = optimizer.optimize(f, PARAM_SPEC)

    assert args[0].value == 2
    assert args[1].value == 2
    assert minimum == -4


def test_multiprocess_returns_result():
    resources = 2  # read: CPUs
    invoker = MultiProcessInvoker(resources)
    invoker.caller = Caller()
    optimizer = GridSearchOptimizer(invoker)
    args, minimum = optimizer.optimize(f=f, param_spec=PARAM_SPEC, \
                                       return_spec=None, minimize=True)

    assert args[0].value == 2
    assert args[1].value == 2
    assert minimum == -4


def test_singleprocess_returns_result():
    resources = 2  # should get ignored
    invoker = SingleProcessInvoker(resources)
    invoker.caller = Caller()
    optimizer = GridSearchOptimizer(invoker)
    args, minimum = optimizer.optimize(f=f, param_spec=PARAM_SPEC, \
                                       return_spec=None, minimize=True)

    assert args[0].value == 2
    assert args[1].value == 2
    assert minimum == -4


if __name__ == '__main__':
    import nose
    nose.runmodule()
