# -*- coding: utf-8 -*-
"""

This module provides decorators to specify the parameters of a function without
using an explicit ParamSpec object. For example::

    from metaopt.core.paramspec.util.param import param

    @param.int("a", interval=(1, 10), step=2, title="α")
    @param.float("b", interval=(0, 1), title="β")
    @param.bool("g", title="γ")
    def some_function(a, b, c):
        pass

This code specifies that some_function takes 3 parameters ``a``, ``b``, and
``g`` each with their own interval, step size and display name.

"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from functools import partial, wraps

# First Party
from metaopt.core.paramspec.util.exception import MultiMultiParameterError, \
    TitleForMultiParameterError
from metaopt.core.paramspec.util.make_param_spec import make_param_spec


def multi(other_decorator, names=[], titles=[], *vargs, **kwargs):
    if "title" in kwargs:
        raise TitleForMultiParameterError()

    if other_decorator == multi:
        raise MultiMultiParameterError()


    def decorator(func):
        for name in reversed(names):
            other_decorator(name, *vargs, **kwargs)(func)

        return func

    return decorator


def bool(*vargs, **kwargs):
    """
    A decorator that specifies an bool parameter for a function

    See :meth:`metaopt.core.paramspec.ParamSpec.bool` for the allowed
    parameters.

    """
    def decorator(func):
        param_spec = make_param_spec(func)
        param_spec.bool(*vargs, **kwargs)
        return func

    return decorator


def float(*vargs, **kwargs):
    """
    A decorator that specifies a float parameter for a function

    See :meth:`metaopt.core.paramspec.ParamSpec.float` for the allowed
    parameters.

    """

    def decorator(func):
        param_spec = make_param_spec(func)
        param_spec.float(*vargs, **kwargs)
        return func

    return decorator


def int(*vargs, **kwargs):
    """
    A decorator that specifies an int parameter for a function

    See :meth:`metaopt.core.paramspec.ParamSpec.int` for the allowed parameters.

    """

    print(*vargs)

    def decorator(func):
        param_spec = make_param_spec(func)
        param_spec.int(*vargs, **kwargs)
        return func

    return decorator
