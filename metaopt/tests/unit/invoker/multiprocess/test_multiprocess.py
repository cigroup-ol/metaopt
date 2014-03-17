"""
Tests for the multi process invoker.
"""

from __future__ import division, print_function, with_statement

import nose
from nose.tools.nontrivial import raises

from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.functions import f
from metaopt.tests.util.functions import m as failing_f
from metaopt.util.stoppable import StoppedException
from mock import Mock
from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper

f = f  # helps static code checkers identify attributes.
failing_f = failing_f

try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3


class TestMultiProcessInvoker(object):
    """
    Tests for the multi process invoker.
    """

    def __init__(self):
        self._invoker = None

    def setup(self):
        self._invoker = MultiProcessInvoker()

    def teardown(self):
        del self._invoker

    def test_instanciation(self):
        pass

    def test_sane_initiation(self):
        assert not self._invoker.stopped

    def test_protected_attributes(self):
        self._invoker.f = f

        assert self._invoker._lock is not None
        assert self._invoker._queue_outcome is not None
        assert self._invoker._queue_status is not None
        assert self._invoker._queue_task is not None
        assert self._invoker._worker_count_max >= 1

    def test_stop(self):
        self._invoker.stop()
        assert self._invoker.stopped

    @raises(StoppedException)
    def test_repeated_stop_raises_exception(self):
        self._invoker.stop()
        self._invoker.stop()

    @raises(StoppedException)
    def test_invoke_raises_exception_when_stopped(self):
        self._invoker.stop()
        self._invoker.invoke()

    def test_invoke_calls_on_error(self):
        self._invoker.f = failing_f

        self._invoker.param_spec = failing_f.param_spec
        self._invoker.return_spec = None

        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        args = ArgsCreator(failing_f.param_spec).args()

        self._invoker.invoke(caller, args)
        self._invoker.wait()
        self._invoker.stop()

        assert not caller.on_result.called
        assert caller.on_error.called  # TODO: Also test arguments

    def test_invoke_calls_on_result(self, resources=1, invokes=1):
        self._invoker.f = f

        self._invoker.param_spec = f.param_spec
        self._invoker.return_spec = None

        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        args = ArgsCreator(f.param_spec).args()

        for _ in xrange(invokes):
            self._invoker.invoke(caller, args)

        self._invoker.wait()
        self._invoker.stop()

        # assert successful results
        caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)
        # assert workers terminated
        caller.on_error.assert_called()

    def test_invokes_call_on_result(self):
        self._invoker.f = f

        self._invoker.param_spec = f.param_spec

        # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
        self._invoker.return_spec = None

        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        args = ArgsCreator(f.param_spec).args()

        self._invoker.invoke(caller, args)
        self._invoker.wait()
        caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)

        self._invoker.invoke(caller, args)
        self._invoker.wait()
        caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)

        self._invoker.stop()

    def test_invoke_passes_kwargs_result(self):
        self._invoker.f = f
        self._invoker.param_spec = f.param_spec

        # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
        self._invoker.return_spec = None
        # data = dict()
        data = None  # None is a singleton, so we an identical back
        args = ArgsCreator(f.param_spec).args()

        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        self._invoker.invoke(caller, args, data=data)
        self._invoker.wait()
        self._invoker.stop()

        caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args,
            data=data)

    def test_invoke_different_invokers_calls_on_result(self):
        self.test_invoke_calls_on_result()
        self.teardown()
        self.setup()
        self.test_invoke_calls_on_result()

if __name__ == '__main__':
    nose.runmodule()
