"""
Tests for MultiProcessInvoker
"""

from __future__ import division, print_function, with_statement

from mock import Mock

from orges.invoker.multiprocess import MultiProcessInvoker
from orges.core.returnspec import ReturnValuesWrapper
from orges.core.args import ArgsCreator
from orges.core import param


@param.int("a", interval=[0, 10])
def f(a):
    return a

ARGS = ArgsCreator(f.param_spec).args()

def test_invoke_calls_on_result():
    invoker = MultiProcessInvoker()
    invoker.f = f

    invoker.param_spec = f.param_spec
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker.invoke(caller, ARGS)
    invoker.wait()

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), ARGS)

if __name__ == '__main__':
    import nose
    nose.runmodule()
