"""
Tests that a multiprocess invoker's invoke calls on_result of its caller.
"""
from __future__ import division, print_function, with_statement

import nose
from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.functions import f as f

f = f  # helps static code checkers


def test_invoke_calls_on_result(resources=1, invokes=1):
    invoker = MultiProcessInvoker(resources=resources)
    invoker.f = f

    invoker.param_spec = f.param_spec
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    args = ArgsCreator(f.param_spec).args()

    for _ in xrange(invokes):
        invoker.invoke(caller, args)

    invoker.wait()
    invoker.stop()
    del invoker

    # assert successful results
    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)
    # assert workers terminated
    caller.on_error.assert_called()

if __name__ == '__main__':
    nose.runmodule()
