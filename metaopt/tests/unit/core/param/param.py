# -*- coding: utf-8 -*-
"""
Test for param
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from nose.tools import eq_, raises

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.paramspec.util.exception import MultiMultiParameterError, \
    TitleForMultiParameterError


def test_multi_creates_two_params():
    @param.multi(param.int, ["a", "b"], interval=(1, 10))
    def f():
        pass

    assert "a" in f.param_spec.params
    assert "b" in f.param_spec.params

def test_multi_creates_two_params_are_saved_in_order():
    @param.multi(param.int, ["a", "b"], interval=(1, 10))
    def f():
        pass

    eq_(list(f.param_spec.params), ["a", "b"])

def test_multi_creates_two_params_have_interval():
    @param.multi(param.int, ["a", "b"], interval=(1, 10))
    def f():
        pass

    eq_(f.param_spec.params["a"].interval, (1, 10))
    eq_(f.param_spec.params["b"].interval, (1, 10))

@raises(TitleForMultiParameterError)
def test_multi_given_a_title_raises_error():
    @param.multi(param.int, ["a", "b"], interval=(1, 10), title="title")
    def f():
        pass

@raises(MultiMultiParameterError)
def test_multi_using_multi_raises_error():
    @param.multi(param.multi, ["a", "b"], interval=(1, 10))
    def f():
        pass

def test_int_first_param_creates_param_spec():
    @param.int("a", interval=(1, 10))
    def f():
        pass

def test_int_first_param_creates_param_spec():
    @param.int("a", interval=(1, 10))
    def f():
        pass

    assert "a" in f.param_spec.params

def test_int_multiple_params_are_saved():
    @param.int("a", interval=(1, 10))
    @param.int("b", interval=(1, 10))
    def f():
        pass

    assert "a" in f.param_spec.params
    assert "b" in f.param_spec.params

def test_int_multiple_params_are_saved_in_order():
    @param.int("a", interval=(1, 10))
    @param.int("b", interval=(1, 10))
    def f():
        pass

    eq_(list(f.param_spec.params), ["a", "b"])

if __name__ == '__main__':
    nose.runmodule()
