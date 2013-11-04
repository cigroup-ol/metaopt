from nose.tools import eq_

# from orges.invoker.simple import SimpleInvoker
from orges.invoker.multiprocess import MultiProcessInvoker
from orges.invoker.pluggable import PluggableInvoker
from orges.main import custom_optimize
from orges.optimizer.gridsearch import GridSearchOptimizer
import orges.test.utils as utils


def test_custom_optimize_running_too_long_aborts():
    invoker = PluggableInvoker(None, invoker=MultiProcessInvoker())
    optimizer = GridSearchOptimizer()

    f = utils.one_param_sleep_and_negate_f
    val = custom_optimize(f, optimizer=optimizer, invoker=invoker, timeout=1)[1]

    # f(a=0) is 0, f(a=1) is -1. Because of the timeout we never see a=1, hence
    # we except the minimum before the timeout to be 0.
    eq_(val, 0)

if __name__ == '__main__':
    import nose
    nose.runmodule()
