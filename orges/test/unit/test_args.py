from orges.paramspec import ParamSpec

from orges.args import Arg, ArgsCreator
from orges.args import UnboundedArgIterError, NoStepArgIterError

from nose.tools import raises
from nose.tools import eq_

def test_arg_iter_bounded_int_works():
  param_spec = ParamSpec()
  param_spec.int("a").interval((1, 10))

  values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
  eq_(values, list(range(1, 10)))

def test_arg_iter_bounded_int_with_step_works():
  param_spec = ParamSpec()
  param_spec.int("a").interval((1, 10)).step(2)

  values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
  # TODO: Should the upper bound always be included?
  eq_(values, [1, 3, 5, 7, 9, 10])

def test_arg_iter_bool_works():
  param_spec = ParamSpec()
  param_spec.bool("a")

  values = [arg.value for arg in list(Arg(param_spec.params["a"]))]
  eq_(values, [True, False])  

@raises(UnboundedArgIterError)
def test_arg_iter_unbounded_raises_error():
  param_spec = ParamSpec()
  param_spec.float("a")

  list(Arg(param_spec.params["a"]))

@raises(UnboundedArgIterError)
def test_arg_iter_half_bounded_raises_error():
  param_spec = ParamSpec()
  param_spec.float("a").interval((0, None))
  param_spec.float("b").interval((None, 0))

  list(Arg(param_spec.params["a"]))
  list(Arg(param_spec.params["b"]))

@raises(NoStepArgIterError)
def test_arg_iter_no_step_raises_error():
  param_spec = ParamSpec()
  param_spec.float("a").interval((0, 1))
  list(Arg(param_spec.params["a"]))
