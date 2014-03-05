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
from metaopt.invoker.util.worker_provider import WorkerProcessProvider
import multiprocessing

f = f  # helps static code checkers


def test_invoke_calls_on_result():
    print(0)
    invoker = MultiProcessInvoker(resources=1)
    print(1)
    invoker.f = f

    invoker.param_spec = f.param_spec
    invoker.return_spec = None

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    args = ArgsCreator(f.param_spec).args()

    print(0)
    try:
        invoker.invoke(caller, args)
        invoker.invoke(caller, args)
        invoker.invoke(caller, args)
    except Exception as e:
        print(e)
    print(1)
    invoker.wait()
    print(2)
    try:
        invoker.stop()
    except Exception as e:
        print(e)
    print(3)
    del invoker

    multiprocessing.active_children()
    #multiprocessing.current_process().terminate()

    assert WorkerProcessProvider()._worker_processes == []

    caller.on_result.assert_called_with(ReturnValuesWrapper(None, 0), args)
    assert not caller.on_error.called
    print("a")

if __name__ == '__main__':
    print(-1)
    test_invoke_calls_on_result()
    nose.runmodule()
