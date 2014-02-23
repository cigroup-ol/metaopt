"""
Tests for MultiProcessInvoker
"""

from __future__ import division, print_function, with_statement

from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.functions import f as f
from metaopt.tests.util.functions import m as failing_f


def test_invoke_calls_on_result():
    invoker = MultiProcessInvoker()
    invoker.f = f

    invoker.param_spec = f.param_spec
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    args = ArgsCreator(f.param_spec)

    invoker.invoke(caller, args)
    invoker.wait()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)
    assert not caller.on_error.called

def test_invoke_multiple_times_calls_on_result():
    invoker = MultiProcessInvoker()
    invoker.f = f

    invoker.param_spec = f.param_spec

    # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    args = ArgsCreator(f.param_spec).args()

    invoker.invoke(caller, args)
    invoker.wait()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)

    invoker.invoke(caller, args)
    invoker.wait()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)

def test_invoke_different_invokers_calls_on_result():
    test_invoke_calls_on_result()
    test_invoke_calls_on_result()

def test_invoke_given_extra_args_calls_on_result_with_them():
    invoker = MultiProcessInvoker()
    invoker.f = f

    invoker.param_spec = f.param_spec

    # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    data = object()

    args = ArgsCreator(f.param_spec).args()

    invoker.invoke(caller, args, data=data)
    invoker.wait()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args,
        data=data)

def test_invoke_calls_on_error():
    invoker = MultiProcessInvoker()
    invoker.f = failing_f

    invoker.param_spec = failing_f.param_spec
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    args = ArgsCreator(failing_f.param_spec).args()

    invoker.invoke(caller, args)
    invoker.wait()

    assert not caller.on_result.called
    assert caller.on_error.called # TODO: Also test arguments


if __name__ == '__main__':
    import nose
    nose.runmodule()
