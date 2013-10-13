from paramspec import ParamSpec
from inspect import getargspec

import itertools

def call(f, fargs):
  args, vargs, kwargs, _ = getargspec(f)  

  if vargs is not None:
    raise CallNotPossibleError(
      "Functions with variable arguments are not supported")

  if kwargs is not None:
    fkwargs = dict()

    for farg in fargs:
      fkwargs[farg.param.name] = farg.value

    return f(**fkwargs)

  if vargs is None and kwargs is None:
    if len(args) == len(fargs):
      return f(*[farg.value for farg in fargs])      

    if len(args) == 1:
      dargs = dict()

      for farg in fargs:
        dargs[farg.param.name] = farg.value

      return f(dargs)
    else:
      raise CallNotPossibleError(
        "Function expects %s arguments but %s were given."
        % (len(args), len(fargs)))


class CallNotPossibleError(Exception):
  def __init__(self, msg):
    Exception.__init__(self, msg)

class ArgsCreator(object):
  def __init__(self, param_spec):
    self.param_spec = param_spec

  def args(self):
    return [Arg(param) for param in self.param_spec.params.values()]

  def product(self):
    return itertools.product(*self.args())

class Arg(object):
  def __init__(self, param, value=None):
    self.param = param
    self.value = value

    if self.value is None:
      self.value = self.param.interval[0]

  def __iter__(self):
    if self.param.type is "bool":
      return BoolArgIter(self)

    if None in self.param.interval:
      raise UnboundedArgIterError(self.param)

    if self.param.step is None:
      raise NoStepArgIterError(self.param)

    return ArgIter(self)

  def __repr__(self):
    return "%s=%s" % (self.param.name, self.value)

  def default():
    pass

class ArgIter():
  def __init__(self, arg):
    self.arg = arg
    self.stop = False

  def next(self):
    current_arg = self.arg

    if self.arg.value == self.arg.param.interval[1] or self.stop:
      raise StopIteration()

    if self.arg.value > self.arg.param.interval[1]:
      self.stop = True
      return Arg(self.arg.param, self.arg.param.interval[1])

    self.arg = Arg(self.arg.param, self.arg.value + self.arg.param.step)

    return current_arg

  def __next__(self):
    next(self)

class BoolArgIter():
  def __init__(self, arg):
    self.stop = False
    self.arg = arg

  def next(self):
    current_arg = self.arg

    if self.stop:
      raise StopIteration

    if self.arg.value:
      self.arg = Arg(self.arg.param, False)
    else:
      self.stop = True

    return current_arg

  def __next__(self):
    next(self)

class UnboundedArgIterError(Exception):
  """The error that occurs when an iter for an unbounded interval is used"""
  def __init__(self, param):
    Exception.__init__(self, "The interval %s is unbounded for parameter: %s" 
      % (param.interval, param.name))

class NoStepArgIterError(Exception):
  """The error that occurs when an iter with no given step size is used"""
  def __init__(self, param):
    Exception.__init__(self, "No step size specified for parameter: %s" 
      % (param.name,))    

if __name__ == '__main__':
  param_spec = ParamSpec()
  param_spec.int("lambda").interval((1, 3))
  param_spec.int("mu").interval((1, 3))
  param_spec.float("tau").interval((0.0, 1.0)).step(0.1)
  param_spec.bool("flag")

  args_creator = ArgsCreator(param_spec)

  print list(args_creator.product())

