from __future__ import division, print_function, with_statement

from mock import Mock
from nose.tools import eq_

from orges.invoker.pluggable import PluggableInvoker
from orges.args import ArgsCreator
import orges.param as param


@param.int("a", interval=(0, 1))
def f(a):
    return a


def test_before_invoke_calls_plugins():
    mock_plugin = Mock()
    mock_plugin.before_invoke = Mock(spec=[])

    plugins = [mock_plugin]
    stub_invoker = Mock()

    stub_invoker.invoke = Mock(return_value=(None, False))
    stub_invoker.wait = Mock(return_value=False)

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    assert mock_plugin.before_invoke.called


def test_on_invoke_calls_plugins():
    mock_plugin = Mock()
    mock_plugin.on_invoke = Mock(spec=[])

    plugins = [mock_plugin]
    stub_invoker = Mock()

    stub_invoker.invoke = Mock(return_value=(None, False))
    stub_invoker.wait = Mock(return_value=False)

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    assert mock_plugin.on_invoke.called


def test_on_result_calls_plugins():
    stub_caller = Mock()

    mock_plugin = Mock()
    mock_plugin.on_result = Mock(spec=[])

    stub_invoker = Mock()

    stub_invoker.invoke = Mock(return_value=(None, False))
    stub_invoker.wait = Mock(return_value=False)

    plugins = [mock_plugin]

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)
    invoker.caller = stub_caller

    def stub_invoke(f, fargs, **kwargs):
        invoker.on_result(0, fargs, **kwargs)
        return None, False

    stub_invoker.invoke = Mock(spec=[])
    stub_invoker.invoke.side_effect = stub_invoke

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    assert mock_plugin.on_result.called


def test_on_error_calls_plugins():
    stub_caller = Mock()

    mock_plugin = Mock()
    mock_plugin.on_error = Mock(spec=[])

    plugins = [mock_plugin]
    stub_invoker = Mock()
    stub_invoker.wait = Mock(return_value=False)

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)
    invoker.caller = stub_caller

    def stub_invoke(f, fargs, **kwargs):
        invoker.on_error(fargs, **kwargs)
        return None, False

    stub_invoker.invoke = Mock(spec=[])
    stub_invoker.invoke.side_effect = stub_invoke

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    assert mock_plugin.on_error.called


def test_invocation_can_be_retried():
    stub_caller = Mock()
    stub_plugin = Mock()
    mock_invoker = Mock()

    plugins = [stub_plugin]

    invoker = PluggableInvoker(mock_invoker, plugins=plugins)
    invoker.caller = stub_caller

    def stub_invoke(f, fargs, **kwargs):
        invoker.on_result(0, fargs, **kwargs)
        return None, False

    mock_invoker.invoke = Mock(spec=[])
    mock_invoker.invoke.side_effect = stub_invoke

    def stub_on_result(invocation):
        if mock_invoker.invoke.call_count == 1:
            invocation.retry = True
        else:
            invocation.retry = False

    stub_plugin.on_result = Mock()
    stub_plugin.on_result.side_effect = stub_on_result

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    eq_(mock_invoker.invoke.call_count, 2)


def test_invocation_tries_is_saved():
    stub_caller = Mock()
    stub_plugin = Mock()
    mock_invoker = Mock()

    plugins = [stub_plugin]

    invoker = PluggableInvoker(mock_invoker, plugins=plugins)
    invoker.caller = stub_caller

    def stub_invoke(f, fargs, **kwargs):
        invoker.on_result(0, fargs, **kwargs)
        return None, False

    mock_invoker.invoke = Mock(spec=[])
    mock_invoker.invoke.side_effect = stub_invoke

    def stub_on_result(invocation):
        if mock_invoker.invoke.call_count == 1:
            invocation.retry = True
            eq_(invocation.tries, 1)
        else:
            invocation.retry = False
            eq_(invocation.tries, 2)

    stub_plugin.on_result = Mock()
    stub_plugin.on_result.side_effect = stub_on_result

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

if __name__ == '__main__':
    import nose
    nose.runmodule()