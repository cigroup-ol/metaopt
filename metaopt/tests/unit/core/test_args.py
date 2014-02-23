# -*- coding: utf-8 -*-
"""
Tests for the args module.
"""

from __future__ import division, print_function, with_statement

from mock import Mock
from nose.tools import eq_, raises

from metaopt.core.args import Arg, BoolArg, NoStepArgIterError
from metaopt.core.call import CallNotPossibleError, call
from metaopt.core.paramspec import ParamSpec


def test_arg_iter_bounded_int_works():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 10))

    values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
    eq_(values, list(range(1, 11)))


def test_arg_iter_bounded_int_small_interval_works():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))

    values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
    eq_(values, [1, 2])


def test_arg_iter_bounded_int_with_step_works():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 10), step=2)

    values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
    # TODO: Should the upper bound always be included?
    eq_(values, [1, 3, 5, 7, 9, 10])


def test_arg_iter_bool_works():
    param_spec = ParamSpec()
    param_spec.bool("a")

    values = [arg.value for arg in list(BoolArg(param_spec.params["a"]))]
    eq_(values, [True, False])


@raises(NoStepArgIterError)
def test_arg_iter_no_step_raises_error():
    param_spec = ParamSpec()
    param_spec.float("a", interval=(0, 1))
    list(Arg(param_spec.params["a"]))


def test_arg_repr_no_title_shows_name_and_value():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(0, 10))
    eq_(str(Arg(param_spec.params["a"])), "a=0")


def test_arg_repr_title_shows_title_and_value():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(0, 10), title="α")
    eq_(str(Arg(param_spec.params["a"])), "α=0")


if __name__ == '__main__':
    import nose
    nose.runmodule()
