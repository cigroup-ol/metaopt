# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from nose.tools import eq_

# First Party
from metaopt.core.arg.bool import BoolArg
from metaopt.core.paramspec.paramspec import ParamSpec


class TestBoolArg(object):
    def test_arg_iter_bool_works(self):
        param_spec = ParamSpec()
        param_spec.bool("a")

        values = [arg.value for arg in list(BoolArg(param_spec.params["a"]))]
        eq_(values, [True, False])

if __name__ == '__main__':
    nose.runmodule()
