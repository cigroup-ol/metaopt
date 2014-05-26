# -*- coding: utf-8 -*-
"""Decorators for easy creation of ReturnSpec objects"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.returnspec.util.make_returnspec import make_return_spec


def maximize(*vargs, **kwargs):
    def decorator(f):
        return_spec = make_return_spec(f)
        return_spec.maximize(*vargs, **kwargs)
        return f

    return decorator


def minimize(*vargs, **kwargs):
    def decorator(f):
        return_spec = make_return_spec(f)
        return_spec.minimize(*vargs, **kwargs)
        return f

    return decorator
