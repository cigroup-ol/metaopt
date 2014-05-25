# -*- coding: utf-8 -*-
"""
Tests for the args module.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import sys

# Third Party
import nose
from nose.tools import eq_, raises

# First Party
from metaopt.core.arg.arg import Arg
from metaopt.core.arg.util.exception import NoStepArgIterError
from metaopt.core.paramspec.paramspec import ParamSpec


if sys.version_info[0] == 3:
    unicode = str  # @ReservedAssignment


class TestArgs(object):
    def test_arg_iter_bounded_int_works(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 10))

        values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
        eq_(values, list(range(1, 11)))

    def test_arg_iter_bounded_int_small_interval_works(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 2))

        values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
        eq_(values, [1, 2])

    def test_arg_iter_bounded_int_with_step_works(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 10), step=2)

        values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
        # TODO: Should the upper bound always be included?
        eq_(values, [1, 3, 5, 7, 9, 10])

    @raises(NoStepArgIterError)
    def test_arg_iter_no_step_raises_error(self):
        param_spec = ParamSpec()
        param_spec.float("a", interval=(0, 1))
        list(Arg(param_spec.params["a"]))

    def test_arg_repr_no_title_shows_name_and_value(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(0, 10))
        eq_(str(Arg(param_spec.params["a"])), "a=0")

    def test_arg_repr_title_shows_title_and_value(self):
        # setup
        param_spec = ParamSpec()
        param_spec.int("a", interval=(0, 10), title="α")

        # run
        result = unicode(Arg(param_spec.params["a"]))
        expect = "α=0"

        # assert
        eq_(result, expect)


if __name__ == '__main__':
    nose.runmodule()
