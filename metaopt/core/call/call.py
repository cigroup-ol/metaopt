# -*- coding: utf-8 -*-
"""
This module provides methods for calling objective functions
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from inspect import getargspec

# First Party
from metaopt.core.call.util.exception import CallNotPossibleError
from metaopt.core.returnspec.util.wrap_return_values import wrap_return_values


def call(f, fargs, param_spec=None, return_spec=None):
    """Call a function using a list of args"""
    del param_spec  # TODO
    if fargs is None:
        fargs = []

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
