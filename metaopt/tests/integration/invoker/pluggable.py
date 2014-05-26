# -*- coding: utf-8 -*-
"""
Tests for the pluggable invoker.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from mock import Mock
from nose.tools import eq_

# First Party
from metaopt.concurrent.invoker.pluggable import PluggableInvoker
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.returnspec.returnspec import ReturnSpec
from metaopt.objective.integer.fast.implicit.f import f
from metaopt.tests.util.matcher import EqualityMatcher


f = f  # helps static code checkers identify attributes.


class TestPluggable(object):

    def test_before_first_invoke_sets_up_plugins(self):
        stub_invoker = Mock()
        stub_invoker.f = f
        stub_invoker.param_spec = f.param_spec
        stub_invoker.return_spec = ReturnSpec(f)
        stub_invoker.invoke = Mock(return_value=(None))
        stub_invoker.wait = Mock(return_value=False)

        mock_plugin = Mock()
        mock_plugin.setup = Mock()
        plugins = [mock_plugin]

        invoker = PluggableInvoker(stub_invoker, plugins=plugins)
        invoker.f = f

        args = ArgsCreator(f.param_spec).args()
        invoker.invoke(caller=None, fargs=args)

        mock_plugin.setup.assert_called_once_with(
            EqualityMatcher(stub_invoker.f),
            EqualityMatcher(stub_invoker.param_spec),
            EqualityMatcher(stub_invoker.return_spec),
        )

    def test_before_invoke_calls_plugins(self):
        stub_invoker = Mock()
        stub_invoker.f = f
        stub_invoker.invoke = Mock(return_value=(None, False))
        stub_invoker.wait = Mock(return_value=False)

        mock_plugin = Mock()
        mock_plugin.before_invoke = Mock(spec=[])
        plugins = [mock_plugin]

        invoker = PluggableInvoker(stub_invoker, plugins=plugins)
        invoker.f = f

        args = ArgsCreator(f.param_spec).args()
        invoker.invoke(None, args)

        assert mock_plugin.before_invoke.called

    def test_on_invoke_calls_plugins(self):
        mock_plugin = Mock()
        mock_plugin.on_invoke = Mock(spec=[])

        plugins = [mock_plugin]
        stub_invoker = Mock()
        stub_invoker.f = f

        stub_invoker.invoke = Mock(return_value=(None, False))
        stub_invoker.wait = Mock(return_value=False)

        invoker = PluggableInvoker(stub_invoker, plugins=plugins)
        invoker.f = f

        args = ArgsCreator(f.param_spec).args()
        invoker.invoke(None, args)

        assert mock_plugin.on_invoke.called

    def test_on_result_calls_plugins(self):
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

        def stub_invoke(caller, fargs, **kwargs):
            del caller  # TODO
            invoker.on_result(value=0, fargs=fargs, **kwargs)
            return None, False

        invoker.f = f

        stub_invoker.invoke = Mock(spec=[])
        stub_invoker.invoke.side_effect = stub_invoke

        args = ArgsCreator(f.param_spec).args()
        invoker.invoke(caller=stub_caller, fargs=args)

        assert mock_plugin.on_result.called

    def test_on_error_calls_plugins(self):
        stub_caller = Mock()

        mock_plugin = Mock()
        mock_plugin.on_error = Mock(spec=[])

        plugins = [mock_plugin]

        stub_invoker = Mock()
        stub_invoker.f = f
        stub_invoker.wait = Mock(return_value=False)

        invoker = PluggableInvoker(invoker=stub_invoker, plugins=plugins)

        def stub_invoke(caller, fargs, **kwargs):
            del caller  # TODO
            invoker.on_error(value=None, fargs=fargs, **kwargs)
            return None, False

        invoker.f = f

        stub_invoker.invoke = Mock(spec=[])
        stub_invoker.invoke.side_effect = stub_invoke

        args = ArgsCreator(f.param_spec).args()
        invoker.invoke(stub_caller, args)

        assert mock_plugin.on_error.called

    def test_invocation_can_be_retried(self):
        stub_caller = Mock()
        stub_plugin = Mock()

        mock_invoker = Mock()
        mock_invoker.f = f

        plugins = [stub_plugin]

        invoker = PluggableInvoker(invoker=mock_invoker, plugins=plugins)

        def stub_invoke(caller, fargs, **kwargs):
            del caller  # TODO
            invoker.on_result(value=0, fargs=fargs, **kwargs)
            return None, False

        invoker.f = f

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

    def test_invocation_tries_is_saved(self):
        stub_caller = Mock()
        stub_plugin = Mock()

        mock_invoker = Mock()
        mock_invoker.f = f

        plugins = [stub_plugin]

        invoker = PluggableInvoker(invoker=mock_invoker, plugins=plugins)
        invoker.f = f

        def stub_invoke(caller, fargs, **kwargs):
            caller.on_result(value=0, fargs=fargs, **kwargs)
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
