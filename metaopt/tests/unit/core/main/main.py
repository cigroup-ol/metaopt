# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
from nose.tools import raises

# First Party
from metaopt.core.main import NoParamSpecError, custom_optimize
from metaopt.invoker.dualthread import DualThreadInvoker


@raises(NoParamSpecError)
def test_custom_optimize_given_no_param_spec_complains():
    def f(x, y):
        pass

    custom_optimize(f, DualThreadInvoker())
