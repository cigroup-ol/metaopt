from orges.main import custom_optimize, NoParamSpecError

from nose.tools import raises


def f(x, y):
    pass


@raises(NoParamSpecError)
def test_custom_optimize_given_no_param_spec_complains():
    custom_optimize(f)

if __name__ == '__main__':
    import nose
    nose.runmodule()
