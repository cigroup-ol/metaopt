"""
Tests for the main module.
"""

from nose.tools import raises

from orges.core.main import custom_optimize, NoParamSpecError


def f(x, y):
    pass


@raises(NoParamSpecError)
def test_custom_optimize_given_no_param_spec_complains():
    custom_optimize(f)

if __name__ == '__main__':
    import nose
    nose.runmodule()
