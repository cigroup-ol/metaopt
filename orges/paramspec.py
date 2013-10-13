from collections import OrderedDict
from inspect import getargspec
from numbers import Integral

class ParamSpec(object):
  """
  An object describing the parameters of an algorithm.

  A parameter is either a fixed value or a description consisting of a type and
  optionally an interval with an associated step size.

  Parameters are specified using chained method invocations like this::

    # A float parameter named "a" with values between 0 and 1
    param_spec.float("a").interval((0, 1))

    # The values of "a" should only be multiple of 0.1
    param_spec.float("a").interval((0, 1)).step(0.1)

    # A float parameter named "b" with all values being allowed
    param_spec.float("b")

    # The values of "b" should only be changed in steps of size 0.2
    param_spec.float("b").all().step(0.2)

    # A float parameter named "c" with no upper bound
    param_spec.float("c").interval(0, None)

  The order the parameters are specified matters since they are used to invoke
  the actual algorithm. That is, given a function ``f(a, b)`` the parameter "a"
  should be specified before the parameter "b".

  """
  def __init__(self, f=None):
    self._params = OrderedDict()

    if f is not None:
      self.infer_params(f)

  @property
  def params(self):
    """
    The specified parameters as ordered dictionary

    Individual parameters can be accessed by using their name as key. To get all
    parameters as list use the ``values`` method  .

    """
    return self._params

  def add_param(self, param):
    if param.name in self._params:
      raise DuplicateParamError(param)
    self._params[param.name] = param

  def infer_params(self, f):
    args, vargs, kwargs, _ = getargspec(f)

    if vargs is not None:
      raise InferNotPossibleError("Cannot infer parameters for variable arguments.")

    if kwargs is not None:
      raise InferNotPossibleError("Cannot infer parameters for keyword arguments.")

    for arg in args:
      self.add_param(Param(arg, "float"))

  def float(self, name):
    param = Param(name, "float")
    self.add_param(param)
    return FloatInterval(param)

  def int(self, name):
    param = Param(name, "int")
    param._step = 1

    self.add_param(param)
    return IntInterval(param)

  def bool(self, name):
    param = Param(name, "bool")
    param._interval = (True, False)
    self.add_param(param)
    return None

class DuplicateParamError(Exception):
  """The error that occurs when two parameters with the same name are specified."""

  def __init__(self, param):
    Exception.__init__(self, "Duplicate parameter: %s" % (param.name,))
    self.param = param

class NonIntIntervalError(Exception):
  """The error that occurs when a non-intergral bound is specified"""

  def __init__(self, param, interval, index):
    Exception.__init__(self,
      "Interval [%s, %s] contains non-interger for parameter: %s"
      % (interval[0], interval[1], param.name))
    self.param = param

class NonIntStepError(Exception):
  """The error that occurs when a non-integral is specified"""

  def __init__(self, param, step):
    Exception.__init__(self,
      "Step size (%s) is not an integer for parameter: %s"
      % (step, param.name))
    self.param = param

class InvalidIntervalError(Exception):
  """The error that occurs when an invalid interval is specified"""

  def __init__(self, param, interval):
    Exception.__init__(self,
      "Lower bound (%s) is larger than upper bound (%s) for parameter: %s"
      % (interval[0], interval[1], param.name))
    self.param = param

class InferNotPossibleError(Exception):
  """The error that occurs when parameters cannot be infered"""
  def __init__(self, msg):
    Exception.__init__(self, msg)

class Param(object):
  """A specified parameter consisting of a type, an interval and a step."""

  def __init__(self, name, type):
    self._name = name
    self._type = type

    self._interval = (None, None)
    self._step = None

  @property
  def name(self):
    """The name of the parameter """
    return self._name

  @property
  def type(self):
    """
    The type of the parameter.

    It can be one of the following values: float.

    """
    return self._type

  @property
  def interval(self):
    """
    The interval specifying the allowed values of the parameter

    The interval is either a pair (from, to) that represents the closed interval
    [from, to] or None specifying that all values are valid. If ``from`` or
    ``to`` is None there is no lower or upper bound.

    """
    return self._interval

  @property
  def step(self):
    """
    The step size of the parameter.

    The step size represents the smallest meaningful change in the value of the
    parameter. A smaller change than the step size is expected to have no
    significant effect on the outcome of the algorithm or might not be even
    valid.

    """
    return self._step

class FloatInterval(object):
  def __init__(self, param):
    self.param = param

  def interval(self, interval):
    if interval[0] is not None and interval[1] is not None\
       and interval[0] > interval[1]:
      raise InvalidIntervalError(self.param, interval)

    self.param._interval = interval
    return FloatStep(self.param)

  def all(self):
    return FloatStep(self.param)

class FloatStep(object):
  def __init__(self, param):
    self.param = param

  def step(self, step):
    self.param._step = step
    return None

class IntInterval(object):
  def __init__(self, param):
    self.param = param

  def interval(self, interval):
    if interval[0] is not None and not isinstance(interval[0], Integral):
      raise NonIntIntervalError(self.param, interval, 0)

    if interval[1] is not None and not isinstance(interval[1], Integral):
      raise NonIntIntervalError(self.param, interval, 1)

    if interval[0] is not None and interval[1] is not None\
       and interval[0] > interval[1]:
      raise InvalidIntervalError(self.param, interval)

    self.param._interval = interval
    return IntStep(self.param)

  def all(self):
    return IntStep(self.param)

class IntStep(object):
  def __init__(self, param):
    self.param = param

  def step(self, step):
    if not isinstance(step, Integral):
      raise NonIntStepError(self.param, step)

    self.param._step = step
    return None

if __name__ == '__main__':
  pass
