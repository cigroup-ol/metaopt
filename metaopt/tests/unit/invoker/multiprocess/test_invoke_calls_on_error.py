"""
Tests that a multiprocess invoker's invoke calls its caller's on_error.
"""
from __future__ import division, print_function, with_statement

from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.functions import m as failing_f

failing_f = failing_f  # helps static code checkers


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
    invoker.stop()
    invoker.wait()

    assert not caller.on_result.called
    assert caller.on_error.called  # TODO: Also test arguments

if __name__ == '__main__':
    import nose
    nose.runmodule()
