# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
from nose.tools import eq_

# First Party
from metaopt.core.arg.bool import BoolArg
from metaopt.core.param.paramspec import ParamSpec


def test_arg_iter_bool_works():
    param_spec = ParamSpec()
    param_spec.bool("a")

    values = [arg.value for arg in list(BoolArg(param_spec.params["a"]))]
    eq_(values, [True, False])
