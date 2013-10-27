from mock import Mock

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

    invoker = PluggableInvoker(None, stub_invoker, plugins=plugins)

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    assert mock_plugin.before_invoke.called

def test_on_invoke_calls_plugins():
    mock_plugin = Mock()
    mock_plugin.on_invoke = Mock(spec=[])

    plugins = [mock_plugin]
    stub_invoker = Mock()

    invoker = PluggableInvoker(None, stub_invoker, plugins=plugins)

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    assert mock_plugin.on_invoke.called

def test_on_result_calls_plugins():
    stub_caller = Mock()

    mock_plugin = Mock()
    mock_plugin.on_result = Mock(spec=[])

    plugins = [mock_plugin]
    stub_invoker = Mock()

    invoker = PluggableInvoker(None, stub_invoker, plugins=plugins)
    invoker.caller = stub_caller

    def stub_invoke(f, fargs, **kwargs):
        invoker.on_result(0, fargs, **kwargs)

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

    invoker = PluggableInvoker(None, stub_invoker, plugins=plugins)
    invoker.caller = stub_caller

    def stub_invoke(f, fargs, **kwargs):
        invoker.on_error(fargs, **kwargs)

    stub_invoker.invoke = Mock(spec=[])
    stub_invoker.invoke.side_effect = stub_invoke

    args = ArgsCreator(f.param_spec).args()
    invoker.invoke(f, args)

    assert mock_plugin.on_error.called

if __name__ == '__main__':
    import nose
    nose.runmodule()