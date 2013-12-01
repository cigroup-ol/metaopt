from __future__ import division, print_function, with_statement

from mock import Mock

from orges import param
from orges.args import ArgsCreator
from orges.invoker.simple import SimpleInvoker

@param.int("a", interval=(1, 10))
@param.int("b", interval=(1, 10))
def f(a, b):
    return a + b

ARGS = ArgsCreator(f.param_spec).args()


def test_invoke_calls_on_result():
    invoker = SimpleInvoker()

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker._caller = caller
    invoker.invoke(f, ARGS)
    invoker.wait()

    caller.on_result.assert_called_with(2, ARGS)

def test_invoke_given_extra_args_calls_on_result_with_them():
    invoker = SimpleInvoker()

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

