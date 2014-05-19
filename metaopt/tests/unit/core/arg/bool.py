from metaopt.core.arg.bool import BoolArg
from metaopt.core.param.paramspec import ParamSpec

from nose.tools import eq_


def test_arg_iter_bool_works():
    param_spec = ParamSpec()
    param_spec.bool("a")

    values = [arg.value for arg in list(BoolArg(param_spec.params["a"]))]
    eq_(values, [True, False])
