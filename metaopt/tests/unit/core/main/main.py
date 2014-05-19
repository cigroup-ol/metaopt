from metaopt.core.main import custom_optimize, NoParamSpecError
from metaopt.invoker.dualthread import DualThreadInvoker

from nose.tools import raises


@raises(NoParamSpecError)
def test_custom_optimize_given_no_param_spec_complains():
    def f(x, y):
        pass

    custom_optimize(f, DualThreadInvoker())
