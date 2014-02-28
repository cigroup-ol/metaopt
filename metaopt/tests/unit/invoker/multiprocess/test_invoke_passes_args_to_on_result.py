"""
Tests that a multiprocess invoker's invoke passes given extra args to its
caller's on_result.
"""
from __future__ import division, print_function, with_statement

from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.functions import m as failing_f

failing_f = failing_f  # helps static code checkers


def test_invoke_passes_kwargs_result():
    invoker = MultiProcessInvoker()
    invoker.f = failing_f

    invoker.param_spec = failing_f.param_spec

    # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    data = object()

    args = ArgsCreator(failing_f.param_spec).args()

    invoker.invoke(caller, args, data=data)
    invoker.wait()
    invoker.stop()

    caller.on_error.assert_called_with(ReturnValuesWrapper(None, 0), args,
        data=data)

if __name__ == '__main__':
    import nose
    nose.runmodule()
