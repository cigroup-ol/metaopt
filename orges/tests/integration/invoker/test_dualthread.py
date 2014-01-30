"""
Tests for the multithreaded invoker.
"""

from __future__ import division, print_function, with_statement

from mock import Mock

from orges.core import param
from orges.core.args import ArgsCreator
from orges.core.returnspec import ReturnValuesWrapper
from orges.invoker.dualthread import DualThreadInvoker


@param.int("a", interval=(1, 10))
@param.int("b", interval=(1, 10))
def f(a, b):
    return a + b

ARGS = ArgsCreator(f.param_spec).args()


def test_invoke_calls_on_result():
    invoker = DualThreadInvoker()
    invoker.f = f

    invoker.param_spec = f.param_spec

    # invoker.return_spec = ReturnSpec(f)  # TODO: Fix problems with equality
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker.invoke(caller, ARGS)
    invoker.wait()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 2), ARGS)

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

    invoker.invoke(caller, ARGS, data=data)
    invoker.wait()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 2),
        ARGS, data=data)

if __name__ == '__main__':
    import nose
    nose.runmodule()
