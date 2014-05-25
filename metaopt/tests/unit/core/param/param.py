# -*- coding: utf-8 -*-
"""
Test for param
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from nose.tools import eq_

# First Party
from metaopt.core.paramspec.util import param


class TestParam(object):
    def test_int_first_param_creates_param_spec(self):
        @param.int("a", interval=(1, 10))
        def f():
            pass

        assert "a" in f.param_spec.params

    def test_int_multiple_params_are_saved(self):
        @param.int("a", interval=(1, 10))
        @param.int("b", interval=(1, 10))
        def f():
            pass

        assert "a" in f.param_spec.params
        assert "b" in f.param_spec.params

    def test_int_multiple_params_are_saved_in_order(self):
        @param.int("a", interval=(1, 10))
        @param.int("b", interval=(1, 10))
        def f():
            pass

        eq_(list(f.param_spec.params), ["a", "b"])

if __name__ == '__main__':
    nose.runmodule()
