from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from mock import Mock

from orges.paramspec import ParamSpec
from orges.args import ArgsCreator
from orges.invoker.multiprocess import MultiProcessInvoker


def f(a, b):
    return a + b


PARAM_SPEC = ParamSpec()
PARAM_SPEC.int("a", interval=(1, 10))
PARAM_SPEC.int("b", interval=(1, 10))

ARGS_CREATOR = ArgsCreator(PARAM_SPEC)
ARGS = ARGS_CREATOR.args()


def test_invoke_calls_on_result():
    invoker = MultiProcessInvoker(1, f)

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker._caller = caller
    invoker.invoke(f, ARGS)
    invoker.wait()

    caller.on_result.assert_called_with(2, ARGS)


def test_invoke_given_extra_args_calls_on_result_with_them():
    invoker = MultiProcessInvoker(1, f)

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker._caller = caller

    data = object()

    invoker.invoke(f, ARGS, data=data)
    invoker.wait()

    caller.on_result.assert_called_with(2, ARGS, data=data)

if __name__ == '__main__':
    import nose
    nose.runmodule()

