"""
Integration tests for the multiprocess invoker.
"""
from __future__ import division, print_function, with_statement

import nose
from mock import Mock

from metaopt.core.args import ArgsCreator
from metaopt.core.returnspec import ReturnSpec, ReturnValuesWrapper
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.optimizer.singleinvoke import SingleInvokeOptimizer
from metaopt.tests.util.function.integer.fast. \
    implicit import FUNCTIONS_FAST_IMPLICIT


def test_invoke_calls_on_result():
    for function in FUNCTIONS_FAST_IMPLICIT[:1]:  # TODO test all functions
        print(function)  # log

        caller = Mock()
        caller.on_result = Mock()
        caller.on_error = Mock()

        invoker = MultiProcessInvoker(resources=1)
        invoker.f = function
        invoker.param_spec = function.param_spec
        invoker.return_spec = ReturnSpec(function)

        args = ArgsCreator(function.param_spec).args()
        invoker.invoke(caller=caller, fargs=args)
        invoker.wait()

        caller.on_result.assert_called_once_with(
            value=ReturnValuesWrapper(None, 0),
            fargs=ArgsCreator(function.param_spec).args(),
        )
        assert not caller.on_error.called

        del invoker


def test_optimizer_on_result():
    optimizer = SingleInvokeOptimizer()
    optimizer.on_result = Mock()
    optimizer.on_error = Mock()

    invoker = MultiProcessInvoker()

    for function in FUNCTIONS_FAST_IMPLICIT[:1]:
        invoker.f = function
    optimizer.optimize(invoker=invoker, function=function,
                       param_spec=function.param_spec, return_spec=None)

    args = ArgsCreator(function.param_spec).args()

    assert not optimizer.on_error.called
    optimizer.on_result.assert_called_with(value=ReturnValuesWrapper(None, 0),
                                           fargs=args)


# THIS TEST DOESN'T WORK
# def test_invoke_given_extra_args_calls_on_result_with_them():
#     for function in FUNCTIONS_INTEGER_FAST[:1]:  # TODO test all functions
#         print(function)  # log

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
#         print(function)  # log

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
    nose.runmodule()
