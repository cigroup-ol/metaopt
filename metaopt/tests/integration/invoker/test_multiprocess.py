"""
Tests for the multiprocess invoker.
"""
from __future__ import division, print_function, with_statement

from time import sleep

from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.invoker.util.determine_package import determine_package
from metaopt.tests.util.functions import FUNCTIONS_INTEGER_WORKING


def f():
    """Function that hangs indefinitely."""
    while True:
        sleep(1)


def test_invoke_calls_on_result():
    for function in FUNCTIONS_INTEGER_WORKING[:1]:  # TODO test all functions
        print(function, determine_package(function))

        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()
        invoker = MultiProcessInvoker(resources=1)
        invoker.f = function

        invoker.invoke(caller, ArgsCreator(function.param_spec).args())
        invoker.wait()

        assert not caller.on_error.called
        caller.on_result.assert_called_once_with(
            ReturnValuesWrapper(None, 0),
            ArgsCreator(function.param_spec).args(),
        )

# THIS TEST DOESN'T WORK
# def test_invoke_given_extra_args_calls_on_result_with_them():
#     for function in FUNCTIONS_INTEGER_WORKING[:1]:  # TODO test all functions
#         print(function, determine_package(function))

#         caller = Mock()
#         caller.on_result = Mock()
#         caller.on_error = Mock()

#         invoker = MultiProcessInvoker(resources=1)  # TODO fails in parallel
#         invoker.f = function

#         data = dict()
#         invoker.invoke(caller, ArgsCreator(function.param_spec).args(),
#                        data=data)
#         invoker.wait()

#         assert not caller.on_error.called
#         caller.on_result.assert_called_once_with(
#             0,
#             ArgsCreator(function.param_spec).args(),
#             data=data
#         )


# def test_invoke_not_successful_calls_on_error():
#     for function in FUNCTIONS_INTEGER_FAILING[:1]:  # TODO test all functions
#         print(function, determine_package(function))

#         caller = Mock()
#         caller.on_result = Mock()
#         caller.on_error = Mock()
#         invoker = MultiProcessInvoker(resources=1)  # TODO fails in parallel
#         invoker.f = function

#         data = dict()
#         invoker.invoke(caller, ArgsCreator(function.param_spec).args(),
#                        data=data)
#         invoker.wait()

#         assert caller.on_error.called

if __name__ == '__main__':
    import nose
    nose.runmodule()
