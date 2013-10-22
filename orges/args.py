"""

This module is responsible for creating actual args from params that are defined
in a paramspec and also provides the means to alter these args such as
randomizing.

An arg is something that contains a value that respects the contraints (e.g.
interval with step size) defined by the corresponding param.

For instance, given an int param like ``param_spec.int("a").interval((1,10))`` a
corresponding arg could be something like ``a=1``.

"""

from __future__ import division
from __future__ import print_function

from inspect import getargspec

import itertools
import random


def call(f, fargs):
    """Call a function using a list of args"""

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
    """This class provides the means to create args in different useful ways"""
    def __init__(self, param_spec):
        self.param_spec = param_spec

    def args(self):
        return [create_arg(param) for param in self.param_spec.params.values()]

    def combine(self, args1, args2):
        f = lambda arg1, arg2: Arg(arg1.param, (arg1.value + arg2.value) / 2)
        return map(f, args1, args2)

    def randomize(self, args, sigmas):
        f = lambda arg, sigma: Arg(arg.param, arg.value + random.gauss(0, sigma))
        return map(f, args, sigmas)

    def random(self):
        return [arg.random() for arg in self.args()]

    def product(self):
        """Iterator that iterates over all args combinations"""
        return itertools.product(*self.args())

def create_arg(param, value=None):
    """Factory method for creating args from params"""

    if (param.type == "bool"):
        return BoolArg(param, value)
    else:
        return Arg(param, value)

class Arg(object):
    def __init__(self, param, value=None):
        self.param = param
        self.value = value

        if self.value is None:
            self.value = self.param.interval[0]

    def random(self):
        return Arg(self.param, random.gauss(0, 1))

    def __iter__(self):
        if None in self.param.interval:
            raise UnboundedArgIterError(self.param)

        if self.param.step is None:
            raise NoStepArgIterError(self.param)

        current = self

        while current.value < current.param.interval[1]:
            yield current
            current = Arg(current.param, current.value + current.param.step)

        yield Arg(self.param, self.param.interval[1])

    def __repr__(self):
        return "%s=%s" % (self.param.display_name, self.value)

class BoolArg(Arg):
    def __init__(self, param, value=None):
        Arg.__init__(self, param, value)

    def __iter__(self):
        if self.value:
            yield BoolArg(self.param, True)
        yield BoolArg(self.param, False)

class UnboundedArgIterError(Exception):
    """The error that occurs when an iter for an unbounded interval is used"""
    def __init__(self, param):
        Exception.__init__(
            self,
            "The interval %s is unbounded for parameter: %s"
            % (param.interval, param.name)
        )


class NoStepArgIterError(Exception):
    """The error that occurs when an iter with no given step size is used"""
    def __init__(self, param):
        Exception.__init__(
            self,
            "No step size specified for parameter: %s"
            % (param.name,)
        )
