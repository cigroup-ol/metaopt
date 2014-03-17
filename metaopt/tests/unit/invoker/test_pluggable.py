"""
Tests for the pluggable invoker.
"""

from __future__ import division, print_function, with_statement

import nose
from mock import Mock
from nose.tools import eq_

from metaopt.core.args import ArgsCreator
from metaopt.invoker.pluggable import PluggableInvoker
from metaopt.tests.util.functions import f

f = f  # helps static code checkers identify attributes.


def test_before_first_invoke_sets_up_plugins():
    mock_plugin = Mock()
    mock_plugin.setup = Mock()

    plugins = [mock_plugin]
    stub_invoker = Mock()

    stub_invoker.f = f

    stub_invoker.param_spec = object()
    stub_invoker.return_spec = object()

    stub_invoker.invoke = Mock(return_value=(None))
    stub_invoker.wait = Mock(return_value=False)

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(None, args)

    mock_plugin.setup.assert_called_once_with(
        stub_invoker.f,
        stub_invoker.param_spec,
        stub_invoker.return_spec,
    )


def test_before_invoke_calls_plugins():
    mock_plugin = Mock()
    mock_plugin.before_invoke = Mock(spec=[])

    plugins = [mock_plugin]
    stub_invoker = Mock()
    stub_invoker.f = f

    stub_invoker.invoke = Mock(return_value=(None, False))
    stub_invoker.wait = Mock(return_value=False)

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(None, args)

    assert mock_plugin.before_invoke.called


def test_on_invoke_calls_plugins():
    mock_plugin = Mock()
    mock_plugin.on_invoke = Mock(spec=[])

    plugins = [mock_plugin]
    stub_invoker = Mock()
    stub_invoker.f = f

    stub_invoker.invoke = Mock(return_value=(None, False))
    stub_invoker.wait = Mock(return_value=False)

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(None, args)

    assert mock_plugin.on_invoke.called


def test_on_result_calls_plugins():
    stub_caller = Mock()

    mock_plugin = Mock()
    mock_plugin.on_result = Mock(spec=[])

    stub_invoker = Mock()
    stub_invoker.f = f

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
    invoker.invoke(stub_caller, args)

    assert mock_plugin.on_result.called


def test_on_error_calls_plugins():
    stub_caller = Mock()

    mock_plugin = Mock()
    mock_plugin.on_error = Mock(spec=[])

    plugins = [mock_plugin]

    stub_invoker = Mock()
    stub_invoker.f = f
    stub_invoker.wait = Mock(return_value=False)

    invoker = PluggableInvoker(stub_invoker, plugins=plugins)

    def stub_invoke(f, fargs, **kwargs):
        invoker.on_error(None, fargs, **kwargs)
        return None, False

    stub_invoker.invoke = Mock(spec=[])
    stub_invoker.invoke.side_effect = stub_invoke

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(stub_caller, args)

    assert mock_plugin.on_error.called


def test_invocation_can_be_retried():
    stub_caller = Mock()
    stub_plugin = Mock()

    mock_invoker = Mock()
    mock_invoker.f = f

    plugins = [stub_plugin]

    invoker = PluggableInvoker(mock_invoker, plugins=plugins)

    def stub_invoke(caller, fargs, **kwargs):
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
    invoker.invoke(stub_caller, args)

    eq_(mock_invoker.invoke.call_count, 2)


def test_invocation_tries_is_saved():
    stub_caller = Mock()
    stub_plugin = Mock()

    mock_invoker = Mock()
    mock_invoker.f = f

    plugins = [stub_plugin]

    invoker = PluggableInvoker(mock_invoker, plugins=plugins)

    def stub_invoke(caller, fargs, **kwargs):
        caller.on_result(0, fargs, **kwargs)
        return None

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
    invoker.invoke(stub_caller, args)

if __name__ == '__main__':
    nose.runmodule()
