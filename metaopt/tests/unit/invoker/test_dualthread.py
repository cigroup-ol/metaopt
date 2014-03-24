"""
Tests for the dual-threaded invoker.
"""

from __future__ import division, print_function, with_statement

import nose
from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper
from metaopt.invoker.dualthread import DualThreadInvoker
from metaopt.tests.util.function.integer.failing.f import f as failing_f
from metaopt.tests.util.function.integer.fast.implicit.f import f as f

f = f  # helps static code checkers
failing_f = failing_f  # helps static code checkers


def test_invoke_calls_on_result():
    invoker = DualThreadInvoker()
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


def test_invoke_multiple_times_calls_on_result():
    invoker = DualThreadInvoker()
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
    invoker = DualThreadInvoker()
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
    invoker = DualThreadInvoker()
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
    assert caller.on_error.called  # TODO: Also test arguments

if __name__ == '__main__':
    nose.runmodule()
