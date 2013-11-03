"""
Tests for the MultiprocessInvoker.
"""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from mock import Mock

from orges.paramspec import ParamSpec
from orges.args import ArgsCreator
from orges.invoker.multiprocess import MultiProcessInvoker
from orges.test.unit.invoker.Matcher import EqualityMatcher as Matcher


def f(a, b):
    return a + b

PARAM_SPEC = ParamSpec()
PARAM_SPEC.int("a", interval=(1, 10))
PARAM_SPEC.int("b", interval=(1, 10))

ARGS_CREATOR = ArgsCreator(PARAM_SPEC)
ARGS = ARGS_CREATOR.args()


def test_invoke_calls_on_result():
    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = MultiProcessInvoker(resources=1)
    invoker.caller = caller
    invoker.invoke(f, ARGS)
    invoker.wait()

    caller.on_result.assert_called_once_with(Matcher(2), Matcher(ARGS))


def test_invoke_given_extra_args_calls_on_result_with_them():
    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = MultiProcessInvoker(resources=2)
    invoker.caller = caller
    data = dict()
    invoker.invoke(f, ARGS, data=data)
    invoker.wait()

    caller.on_result.assert_called_once_with(Matcher(2), Matcher(ARGS),
                                             data=Matcher(data))

if __name__ == '__main__':
    import nose
    nose.runmodule()
