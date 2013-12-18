# -*- coding: utf-8 -*-
"""
Tests for the args module.
"""

from __future__ import division, print_function, with_statement

from mock import Mock
from nose.tools import eq_, raises

from orges.core.args import Arg, call, BoolArg, NoStepArgIterError, \
    CallNotPossibleError
from orges.core.paramspec import ParamSpec


def test_call_func_with_args_works():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))
    param_spec.int("b", interval=(1, 2))

    param_a = param_spec.params["a"]
    param_b = param_spec.params["b"]

    arg_a = Arg(param_a, 0)
    arg_b = Arg(param_b, 1)

    f_mock = Mock()

    def f(a, b):    # That's a hack since getargspec doesn't work with mocks
        f_mock(a, b)

    call(f, [arg_a, arg_b])

    f_mock.assert_called_with(arg_a.value, arg_b.value)


def test_call_func_with_single_arg_works():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))

    param_a = param_spec.params["a"]

    arg_a = Arg(param_a, 0)

    f_mock = Mock()

    def f(a):    # That's a hack since getargspec doesn't work with mocks
        f_mock(a)

    call(f, [arg_a])

    f_mock.assert_called_with(arg_a.value)


def test_call_func_with_dict_args_works():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))
    param_spec.int("b", interval=(1, 2))

    param_a = param_spec.params["a"]
    param_b = param_spec.params["b"]

    arg_a = Arg(param_a, 0)
    arg_b = Arg(param_b, 1)

    f_mock = Mock()

    def f(args):    # That's a hack since getargspec doesn't work with mocks
        f_mock(args)

    call(f, [arg_a, arg_b])

    f_mock.assert_called_with({"a": arg_a.value, "b": arg_b.value})


def test_call_func_with_kwargs_works():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))
    param_spec.int("b", interval=(1, 2))

    param_a = param_spec.params["a"]
    param_b = param_spec.params["b"]

    arg_a = Arg(param_a, 0)
    arg_b = Arg(param_b, 1)

    f_mock = Mock()

    def f(**kwargs):
        f_mock(**kwargs)

    call(f, [arg_a, arg_b])

    f_mock.assert_called_with(a=arg_a.value, b=arg_b.value)


def test_call_func_with_args_returns_result():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))
    param_spec.int("b", interval=(1, 2))

    param_a = param_spec.params["a"]
    param_b = param_spec.params["b"]

    arg_a = Arg(param_a, 0)
    arg_b = Arg(param_b, 1)

    def f(a, b):    # That's a hack since getargspec doesn't work with mocks
        return a + b

    assert arg_a.value + arg_b.value == call(f, [arg_a, arg_b])


@raises(CallNotPossibleError)
def test_call_func_with_vargs_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))
    param_spec.int("b", interval=(1, 2))

    param_a = param_spec.params["a"]
    param_b = param_spec.params["b"]

    arg_a = Arg(param_a, 0)
    arg_b = Arg(param_b, 1)

    def f(*vargs):
        pass

    call(f, [arg_a, arg_b])


@raises(CallNotPossibleError)
def test_call_func_with_incorrect_number_of_args_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 2))
    param_spec.int("b", interval=(1, 2))

    param_a = param_spec.params["a"]
    param_b = param_spec.params["b"]

    arg_a = Arg(param_a, 0)
    arg_b = Arg(param_b, 1)

    def f(a, b, c):
        pass

    call(f, [arg_a, arg_b])


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
