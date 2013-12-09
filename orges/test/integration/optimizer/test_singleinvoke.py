"""
TODO document me
"""
from __future__ import division, print_function, with_statement

from mock import Mock

from orges.optimizer.singleinvoke import SingleInvokeOptimizer
from orges.invoker.singleprocess import SingleProcessInvoker
from orges.args import ArgsCreator
from orges.test.integration.invoker.Matcher import EqualityMatcher as Matcher
from orges import param


@param.int("a", interval=(2, 2))
@param.int("b", interval=(1, 1))
def f(a, b):
    return -(a + b)

ARGS = ArgsCreator(f.param_spec).args()


def test_optimize_returns_result():
    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = SingleProcessInvoker()
    optimizer = SingleInvokeOptimizer()

    optimizer.invoker = invoker
    optimizer.invoker.caller = caller

    optimizer.optimize(f, f.param_spec, None)

    invoker.caller.on_error.assert_not_called()
    invoker.caller.on_result.assert_called()
    invoker.caller.on_result.assert_called_with(Matcher(-3), Matcher(ARGS), {})

if __name__ == '__main__':
    import nose
    nose.runmodule()
