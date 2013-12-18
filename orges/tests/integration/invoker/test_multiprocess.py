"""
Tests for the multiprocess invoker.
"""
from __future__ import division, print_function, with_statement

from orges.tests.integration.invoker.util import EqualityMatcher as Matcher

from mock import Mock

from orges.core import param
from orges.core.args import ArgsCreator
from orges.invoker.multiprocess import MultiProcessInvoker


@param.int("a", interval=(1, 10))
@param.int("b", interval=(1, 10))
def f(a, b):
    return a + b

F_PARAM_SPEC = f.param_spec
F_ARGS = ArgsCreator(F_PARAM_SPEC).args()


def test_invoke_calls_on_result():
    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = MultiProcessInvoker(resources=1)
    invoker.caller = caller

    invoker.invoke(f, F_ARGS)
    invoker.wait()

    assert not caller.on_error.called
    caller.on_result.assert_called_once_with(fargs=Matcher(F_ARGS),
                                             result=Matcher(2),
                                             vargs=(),
                                             kwargs={})


def test_invoke_given_extra_args_calls_on_result_with_them():
    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = MultiProcessInvoker(resources=1)  # TODO fails in parallel
    invoker.caller = caller

    data = dict()
    invoker.invoke(f, F_ARGS, data=data)
    invoker.wait()

    assert not caller.on_error.called
    caller.on_result.assert_called_once_with(fargs=Matcher(F_ARGS),
                                             result=Matcher(2),
                                             vargs=(), kwargs=Matcher(data))


@param.int("a", interval=(1, 10))
@param.int("b", interval=(1, 10))
def failing(a, b):
    raise Exception()

FAILING_PARAM_SPEC = failing.param_spec
FAILING_ARGS = ArgsCreator(FAILING_PARAM_SPEC).args()


def test_invoke_not_successful_calls_on_error():
    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = MultiProcessInvoker(resources=1)  # TODO fails in parallel
    invoker.caller = caller

    data = dict()
    invoker.invoke(f, FAILING_ARGS, data=data)
    invoker.wait()

    assert caller.on_error.called

if __name__ == '__main__':
    import nose
    nose.runmodule()
