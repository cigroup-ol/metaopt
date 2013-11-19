"""
TODO document me
"""
from __future__ import division, print_function, with_statement

from mock import Mock

from orges.optimizer.singleinvoke import SingleInvokeOptimizer
from orges.paramspec import ParamSpec
from orges.invoker.singleprocess import SingleProcessInvoker
from orges.args import ArgsCreator
from orges.test.integration.invoker.Matcher import EqualityMatcher as Matcher

f = __name__


def f(a, b):
    return -(a + b)

PARAM_SPEC = ParamSpec()
PARAM_SPEC.int("a", interval=(2, 2))
PARAM_SPEC.int("b", interval=(1, 1))

ARGS = ArgsCreator(PARAM_SPEC).args()


def test_optimize_returns_result():
    resources = 2  # should get ignored

    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = SingleProcessInvoker(resources)
    optimizer = SingleInvokeOptimizer()

    optimizer.invoker = invoker
    optimizer.invoker.caller = caller

    f_package = f
    param_spec = PARAM_SPEC
    return_spec = None
    minimize = True
    optimizer.optimize(f_package, param_spec, return_spec, minimize)

    invoker.caller.on_error.assert_not_called()
    invoker.caller.on_result.assert_called()
    invoker.caller.on_result.assert_called_with(Matcher(-3), Matcher(ARGS), {})

if __name__ == '__main__':
    import nose
    nose.runmodule()
