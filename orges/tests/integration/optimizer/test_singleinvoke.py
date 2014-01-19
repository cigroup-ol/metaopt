"""
TODO document me
"""
from __future__ import division, print_function, with_statement

from mock import Mock

from orges.core import param
from orges.core.args import ArgsCreator
from orges.invoker.singleprocess import SingleProcessInvoker
from orges.optimizer.singleinvoke import SingleInvokeOptimizer


@param.int("a", interval=(2, 2))
@param.int("b", interval=(1, 1))
def f(a, b):
    return -(a + b)

ARGS = ArgsCreator(f.param_spec).args()

def test_optimize_returns_result():
    invoker = SingleProcessInvoker()
    invoker.f = f

    optimizer = SingleInvokeOptimizer()
    optimizer.on_result = Mock()
    optimizer.on_error = Mock()

    optimizer.optimize(invoker, f.param_spec, None)

    assert not optimizer.on_error.called
    optimizer.on_result.assert_called_with(-3, ARGS)

if __name__ == '__main__':
    import nose
    nose.runmodule()
