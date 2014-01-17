"""
This module provides methods for calling objective functions
"""

from inspect import getargspec

from orges.core.returnspec import ReturnValuesWrapper

def call(f, fargs, return_spec=None):
    """Call a function using a list of args"""

    args, vargs, kwargs, _ = getargspec(f)

    if vargs is not None:
        raise CallNotPossibleError(
            "Functions with variable arguments are not supported.")

    if kwargs is not None:
        fkwargs = dict()

        for farg in fargs:
            fkwargs[farg.param.name] = farg.value

        return wrap_return_values(f(**fkwargs), return_spec)

    if vargs is None and kwargs is None:
        if len(args) == len(fargs):
            return wrap_return_values(f(*[farg.value for farg in fargs]),
                return_spec)

        if len(args) == 1:
            dargs = dict()

            for farg in fargs:
                dargs[farg.param.name] = farg.value

            return wrap_return_values(f(dargs), return_spec)
        else:
            raise CallNotPossibleError(
                "Function expects %s arguments but %s were given."
                % (len(args), len(fargs)))

def wrap_return_values(values, return_spec=None):
    if return_spec is None:
        return values

    return ReturnValuesWrapper(return_spec, values)


class CallNotPossibleError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)