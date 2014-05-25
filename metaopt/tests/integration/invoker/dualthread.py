# -*- coding: utf-8 -*-
"""
Tests for the dual-threaded invoker.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from mock import Mock

# First Party
from metaopt.concurrent.invoker.dualthread import DualThreadInvoker
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.returnspec.util.wrapper import ReturnValuesWrapper
from metaopt.objective.integer.failing.f import f as failing_f
from metaopt.objective.integer.fast.implicit.f import f as f


f = f  # helps static code checkers
failing_f = failing_f  # helps static code checkers


class TestDualThreadInvoker(object):
    def __init__(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_invoke_calls_on_result(self):
        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        invoker = DualThreadInvoker()
        invoker.f = f

        invoker.param_spec = f.param_spec
        invoker.return_spec = None
        # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality

        args = ArgsCreator(f.param_spec).args()

        invoker.invoke(caller=caller, fargs=args)
        invoker.wait()

        caller.on_result.assert_called_with(value=ReturnValuesWrapper(None, 0),
                                            fargs=args)

    def test_invoke_multiple_times_calls_on_result(self):
        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        invoker = DualThreadInvoker()
        invoker.f = f

        invoker.param_spec = f.param_spec

        # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
        invoker.return_spec = None

        args = ArgsCreator(f.param_spec).args()

        invoker.invoke(caller=caller, fargs=args)
        invoker.wait()

        caller.on_result.assert_called_with(value=ReturnValuesWrapper(None, 0),
                                            fargs=args)

        invoker.invoke(caller=caller, fargs=args)
        invoker.wait()

        caller.on_result.assert_called_with(value=ReturnValuesWrapper(None, 0),
                                            fargs=args)

    def test_invoke_different_invokers_calls_on_result(self):
        self.test_invoke_calls_on_result()
        self.test_invoke_calls_on_result()

    def test_invoke_given_extra_args_calls_on_result_with_them(self):
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

        caller.on_result.assert_called_with(value=ReturnValuesWrapper(None, 0),
                                            fargs=args, data=data)

    def test_invoke_calls_on_error(self):
        invoker = DualThreadInvoker()
        invoker.f = failing_f

        invoker.param_spec = failing_f.param_spec
        invoker.return_spec = None

        caller = Mock()

        caller.on_result = Mock()
        caller.on_error = Mock()

        args = ArgsCreator(failing_f.param_spec).args()

        invoker.invoke(caller=caller, fargs=args)
        invoker.wait()

        assert not caller.on_result.called
        assert caller.on_error.called  # TODO: Also test arguments

if __name__ == '__main__':
    nose.runmodule()
