"""
Tests that a multiprocess invoker's invoke calls on_result of its caller.
"""
from __future__ import division, print_function, with_statement

import time

from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.functions import f as f

f = f  # helps static code checkers


def test_invoke_calls_on_result():
    invoker = MultiProcessInvoker()
    invoker.f = f

    invoker.param_spec = f.param_spec
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    args = ArgsCreator(f.param_spec).args()

    invoker.invoke(caller, args)
    invoker.wait()
    invoker.stop()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)
    assert not caller.on_error.called

if __name__ == '__main__':
    import nose
    nose.runmodule()
