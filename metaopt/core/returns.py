"""Decorators for easy creation of ReturnSpec objects"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.returnspec import ReturnSpec


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


def make_return_spec(f):
    """
    Create a new return_spec object for ``f`` or retrieves it if it exists.
    """
    try:
        return_spec = f.return_spec
    except AttributeError:
        f.return_spec = return_spec = ReturnSpec(via_decorator=True)
    return return_spec
