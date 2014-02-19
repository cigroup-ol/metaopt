# -!- coding: utf-8 -!-
"""
Test for param_spec
"""
from __future__ import division, print_function, with_statement

from nose.tools import raises

from orges.core.paramspec import DuplicateParamError, InvalidIntervalError, \
    NonIntIntervalError, NonIntStepError, ParamSpec


@raises(Exception)
def test_float_no_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.float("a")


@raises(Exception)
def test_int_no_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a")


def test_float_given_name_saves_by_name():
    param_spec = ParamSpec()
    param_spec.float("a", interval=(0, 1))
    assert "a" in param_spec.params


def test_float_parameter_has_type_float():
    param_spec = ParamSpec()
    param_spec.float("a", interval=(0, 1))
    assert param_spec.params["a"].type == "float"


def test_float_speficied_interval_saves_it():
    param_spec = ParamSpec()
    param_spec.float("a", interval=(-1, 1))
    assert param_spec.params["a"].interval == (-1, 1)


def test_float_speficied_step_saves_it():
    param_spec = ParamSpec()
    param_spec.float("a", interval=(-1, 1), step=0.1)
    assert param_spec.params["a"].step == 0.1


def test_float_multiple_params_are_ordered():
    param_spec = ParamSpec()

    param_spec.float("a", interval=(0, 1))
    param_spec.float("b", interval=(0, 1))
    param_spec.float("c", interval=(0, 1))

    assert list(param_spec.params) == ["a", "b", "c"]


@raises(DuplicateParamError)
def test_float_duplicate_name_raises_error():
    param_spec = ParamSpec()
    param_spec.float("a", interval=(0, 1))
    param_spec.float("a", interval=(0, 1))


@raises(InvalidIntervalError)
def test_float_invalid_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.float("a", interval=(0.1, 0.0))


@raises(InvalidIntervalError)
def test_int_invalid_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(2, 1))


@raises(NonIntIntervalError)
def test_int_float_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(0.1, 0.9))


def test_bool_has_pseudo_interval():
    param_spec = ParamSpec()
    param_spec.bool("a")
    assert param_spec.params["a"].interval == (True, False)


@raises(NonIntStepError)
def test_int_float_step_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 10), step=0.1)


@raises(NonIntIntervalError)
def test_int_invalid_float_interval_raises_float_error():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(0.2, 0.1))


def test_int_given_no_step_defaults_to_one():
    param_spec = ParamSpec()
    param_spec.int("a", interval=(1, 10))
    assert param_spec.params["a"].step == 1


def test_given_no_title_defaults_to_name():
    param_spec = ParamSpec()

    param_spec.int("a", interval=(1, 10))
    param_spec.float("b", interval=(0, 1))
    param_spec.bool("g")

    assert param_spec.params["a"].title == "a"
    assert param_spec.params["b"].title == "b"
    assert param_spec.params["g"].title == "g"


def test_given_title_saves_it():
    param_spec = ParamSpec()

    param_spec.int("a", interval=(1, 10), title="α")
    param_spec.float("b", interval=(0, 1), title="β")
    param_spec.bool("g", title="γ")

    assert param_spec.params["a"].title == "α"
    assert param_spec.params["b"].title == "β"
    assert param_spec.params["g"].title == "γ"

if __name__ == '__main__':
    import nose
    nose.runmodule()
