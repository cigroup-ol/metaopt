from orges.framework.paramspec import ParamSpec
from orges.framework.paramspec import DuplicateParamError, InvalidIntervalError
from orges.framework.paramspec import NonIntIntervalError, NonIntStepError
from orges.framework.paramspec import InferNotPossibleError
from orges.framework.paramspec import FloatInterval, FloatStep

from nose.tools import raises


def test_float_unique_name_asks_for_interval():
    param_spec = ParamSpec()
    obj = param_spec.float("a")
    assert isinstance(obj, FloatInterval)


def test_float_interval_asks_for_step():
    param_spec = ParamSpec()
    need_interval = param_spec.float("a")
    obj = need_interval.interval((0, 1))
    assert isinstance(obj, FloatStep)


def test_float_given_name_saves_by_name():
    param_spec = ParamSpec()
    param_spec.float("a")
    assert "a" in param_spec.params


def test_float_parameter_has_type_float():
    param_spec = ParamSpec()
    param_spec.float("a")
    assert param_spec.params["a"].type == "float"


def test_float_only_name_has_no_interval():
    param_spec = ParamSpec()
    param_spec.float("a")
    assert param_spec.params["a"].interval == (None, None)


def test_all_float_parameter_has_no_interval():
    param_spec = ParamSpec()
    param_spec.float("a").all()
    assert param_spec.params["a"].interval == (None, None)


def test_float_speficied_interval_saves_it():
    param_spec = ParamSpec()
    param_spec.float("a").interval((-1, 1))
    assert param_spec.params["a"].interval == (-1, 1)


def test_float_speficied_step_saves_it():
    param_spec = ParamSpec()
    param_spec.float("a").interval((-1, 1)).step(0.1)
    assert param_spec.params["a"].step == 0.1


def test_float_multiple_params_are_ordered():
    param_spec = ParamSpec()

    param_spec.float("a")
    param_spec.float("b")
    param_spec.float("c")

    assert list(param_spec.params) == ["a", "b", "c"]


@raises(DuplicateParamError)
def test_float_duplicate_name_raises_error():
    param_spec = ParamSpec()
    param_spec.float("a")
    param_spec.float("a")


@raises(InvalidIntervalError)
def test_float_invalid_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.float("a").interval((0.1, 0.0))


@raises(InvalidIntervalError)
def test_int_invalid_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a").interval((2, 1))


@raises(NonIntIntervalError)
def test_int_float_interval_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a").interval((0.1, 0.9))


def test_float_left_bounded_interval_raises_nothing():
    param_spec = ParamSpec()
    param_spec.float("a").interval((0.1, None))


def test_float_right_bounded_interval_raises_nothing():
    param_spec = ParamSpec()
    param_spec.float("a").interval((None, 0.1))


def test_int_left_bounded_interval_raises_nothing():
    param_spec = ParamSpec()
    param_spec.int("a").interval((1, None))


def test_int_right_bounded_interval_raises_nothing():
    param_spec = ParamSpec()
    param_spec.int("a").interval((None, 1))


def test_bool_has_pseudo_interval():
    param_spec = ParamSpec()
    param_spec.bool("a")
    assert param_spec.params["a"].interval == (True, False)


@raises(NonIntStepError)
def test_int_float_step_raises_error():
    param_spec = ParamSpec()
    param_spec.int("a").all().step(0.1)


@raises(NonIntIntervalError)
def test_int_invalid_float_interval_raises_float_error():
    param_spec = ParamSpec()
    param_spec.int("a").interval((0.2, 0.1))


def test_int_given_no_step_defaults_to_one():
    param_spec = ParamSpec()
    param_spec.int("a")
    assert param_spec.params["a"].step == 1


def test_init_given_regular_func_infers_params():
    def f(a, b, c):
        pass

    param_spec = ParamSpec(f)
    assert "a" in param_spec.params
    assert "b" in param_spec.params
    assert "c" in param_spec.params


@raises(InferNotPossibleError)
def test_init_given_kwargs_func_raises_error():
    def f(**kwargs):
        pass

    ParamSpec(f)


@raises(InferNotPossibleError)
def test_init_given_kwargs_and_args_func_raises_error():
    def f(a, b, c, **kwargs):
        pass

    ParamSpec(f)


@raises(InferNotPossibleError)
def test_init_given_vargs_func_raises_error():
    def f(*vargs):
        pass

    ParamSpec(f)


@raises(InferNotPossibleError)
def test_init_given_vargs_and_args_func_raises_error():
    def f(a, b, c, *vargs):
        pass

    ParamSpec(f)


if __name__ == '__main__':
    import nose
    nose.runmodule()
