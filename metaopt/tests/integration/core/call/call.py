# -*- coding: utf-8 -*-
"""
Tests for the call module.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from mock import Mock
from nose.tools import raises

# First Party
from metaopt.core.arg.arg import Arg
from metaopt.core.call.call import call
from metaopt.core.call.util.exception import CallNotPossibleError
from metaopt.core.paramspec.paramspec import ParamSpec
from metaopt.core.returnspec.returnspec import ReturnSpec
from metaopt.core.returnspec.util.wrapper import ReturnValuesWrapper


class TestCall(object):

    def test_call_func_with_return_spec(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 2))

        return_spec = ReturnSpec()
        return_spec.maximize("z")

        def f(a):
            return a

        result = call(f, [Arg(param_spec.params["a"], 1)], param_spec, return_spec)
        assert isinstance(result, ReturnValuesWrapper)

    def test_call_func_with_return_spec_same_str(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 2))

        return_spec = ReturnSpec()
        return_spec.maximize("z")

        def f(a):
            return a

        result = call(f, [Arg(param_spec.params["a"], 1)], return_spec)
        assert str(result) == str(1)

    def test_call_func_without_return_spec(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 2))

        def f(a):
            return a

        result = call(f, [Arg(param_spec.params["a"], 1)])
        assert isinstance(result, ReturnValuesWrapper)

    def test_call_func_with_args_works(self):
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

    def test_call_func_with_single_arg_works(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 2))

        param_a = param_spec.params["a"]

        arg_a = Arg(param_a, 0)

        f_mock = Mock()

        def f(a):    # That's a hack since getargspec doesn't work with mocks
            f_mock(a)

        call(f, [arg_a])

        f_mock.assert_called_with(arg_a.value)

    def test_call_func_with_dict_args_works(self):
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

    def test_call_func_with_kwargs_works(self):
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

    def test_call_func_with_args_returns_result(self):
        param_spec = ParamSpec()
        param_spec.int("a", interval=(1, 2))
        param_spec.int("b", interval=(1, 2))

        param_a = param_spec.params["a"]
        param_b = param_spec.params["b"]

        arg_a = Arg(param_a, 0)
        arg_b = Arg(param_b, 1)

        def f(a, b):    # That's a hack since getargspec doesn't work with mocks
            return a + b

        assert arg_a.value + arg_b.value == call(f, [arg_a, arg_b]).raw_values

    @raises(CallNotPossibleError)
    def test_call_func_with_vargs_raises_error(self):
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
    def test_call_func_with_incorrect_number_of_args_raises_error(self):
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

if __name__ == '__main__':
    nose.runmodule()
