"""
TODO document me
"""
from __future__ import division, print_function, with_statement

from orges.optimizer.gridsearch import GridSearchOptimizer
from orges.paramspec import ParamSpec
from orges.invoker.simple import SimpleInvoker
from mock import Mock
from orges.test.integration.invoker.Matcher import EqualityMatcher as Matcher
from orges.args import ArgsCreator


def f(a, b):
    return -(a + b)

PARAM_SPEC = ParamSpec()
PARAM_SPEC.int("a", interval=(1, 2))
PARAM_SPEC.int("b", interval=(1, 2))

ARGS = ArgsCreator(PARAM_SPEC).product()


def test_optimize_returns_result():
    resources = 2  # should get ignored

    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    _invoker = SimpleInvoker(resources)
    _invoker.caller = caller

    optimizer = GridSearchOptimizer()
    optimizer._invoker = _invoker

    optimizer.optimize(f, PARAM_SPEC)

    caller.on_error.assert_not_called()
    caller.on_result.assert_called_with(Matcher(-4), Matcher(ARGS))

if __name__ == '__main__':
    import nose
    nose.runmodule()
