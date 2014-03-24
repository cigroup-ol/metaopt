"""
Tests that a multiprocess invoker's invoke passes given extra arguments to its
caller's on_result.
"""
from __future__ import division, print_function, with_statement

import nose
from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.function.integer.failing.f import f as f_failing

f_failing = f_failing  # helps static code checkers


def test_invoke_passes_kwargs_result():
    return  # TODO
    invoker = MultiProcessInvoker()
    invoker.f = f_failing

    invoker.param_spec = f_failing.param_spec

    # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    data = object()

    args = ArgsCreator(f_failing.param_spec).args()

    invoker.invoke(caller, args, data=data)
    invoker.wait()
    invoker.stop()

    caller.on_error.assert_called_with(ReturnValuesWrapper(None, 0), args,
        data=data)

if __name__ == '__main__':
    nose.runmodule()
