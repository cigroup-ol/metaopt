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


def call(f, fargs, param_spec, return_spec=None):
    """Call a function using a list of args"""

    if fargs is None:
        fargs = []

    extra_kwargs = param_spec.extra_kwargs or {}

    args, vargs, kwargs, _ = getargspec(f)

    if vargs is not None:
        raise CallNotPossibleError(
            "Functions with variable arguments are not supported.")

    if kwargs is not None:
        fkwargs = dict()

        for farg in fargs:
            fkwargs[farg.param.name] = farg.value

        fkwargs.update(extra_kwargs)

        return wrap_return_values(f(**fkwargs), return_spec)

    if vargs is None and kwargs is None:
        if len(args) == len(fargs) + len(extra_kwargs):
            return wrap_return_values(
                f(*[farg.value for farg in fargs], **extra_kwargs), return_spec
            )
        else:
            raise CallNotPossibleError(
                "Function expects %s arguments but %s were given."
                % (len(args), len(fargs)))
