"""
Integration tests for the multiprocess invoker.
"""
from __future__ import division, print_function, with_statement

import nose
from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnSpec, ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.optimizer.singleinvoke import SingleInvokeOptimizer
from metaopt.tests.util.function.integer.fast.explicit.f import f as f_working
from metaopt.tests.util.function.integer.failing.f import f as f_failing

f_working = f_working
f_failing = f_failing


class TestMultiProcessInvoker(object):
    """
    Integration tests for the multiprocess invoker.
    """

    def __init__(self):
        self._invoker = None

    def setup(self):
        self._invoker = MultiProcessInvoker(resources=1)

    def teardown(self):
        self._invoker.stop()

    def test_instanciation(self):
        self._invoker = MultiProcessInvoker()
        self._invoker.f = f_working
        caller = Mock()
        fargs = {'a': 0}
        self._invoker.invoke(caller=caller, fargs=fargs)
        self._invoker.wait()

    def test_invoke_calls_on_result(self):
        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        self._invoker.f = f_working
        self._invoker.param_spec = f_working.param_spec
        self._invoker.return_spec = ReturnSpec(f_working)

        args = ArgsCreator(f_working.param_spec).args()
        self._invoker.invoke(caller=caller, fargs=args)
        self._invoker.wait()

        caller.on_result.assert_called_once_with(
            value=ReturnValuesWrapper(None, 0),
            fargs=args,
        )
        assert not caller.on_error.called

    def test_optimizer_on_result(self):
        optimizer = SingleInvokeOptimizer()
        optimizer.on_result = Mock()
        optimizer.on_error = Mock()

        self._invoker.f = f_working
        self._invoker.param_spec = f_working.param_spec
        self._invoker.return_spec = ReturnSpec(f_working)

        optimizer.optimize(invoker=self._invoker,
                           param_spec=self._invoker.param_spec,
                           return_spec=self._invoker.return_spec)

        args = ArgsCreator(self._invoker.param_spec).args()

        assert not optimizer.on_error.called
        optimizer.on_result.assert_called_with(value=ReturnValuesWrapper(None, 0),
                                               fargs=args)

    def test_invoke_given_extra_args_calls_on_result_with_them(self):
        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        self._invoker.f = f_working
        self._invoker.param_spec = f_working.param_spec
        self._invoker.return_spec = ReturnSpec(f_working)

        data = None
        args = ArgsCreator(self._invoker.param_spec).args()
        self._invoker.invoke(caller, fargs=args, data=data)
        self._invoker.wait()

        assert not caller.on_error.called
        caller.on_result.assert_called_once_with(value=ReturnValuesWrapper(None, 0),
                                                 fargs=args, data=data)

    def test_invoke_not_successful_calls_on_error(self):
        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        self._invoker.f = f_failing
        self._invoker.param_spec = f_failing.param_spec
        self._invoker.return_spec = ReturnSpec(f_failing)

        data = dict()
        args = ArgsCreator(self._invoker.param_spec).args()

        self._invoker.invoke(caller=caller, fargs=args, data=data)
        self._invoker.wait()

        assert not caller.on_result.called
        assert caller.on_error.called

if __name__ == '__main__':
    nose.runmodule()
