"""
A failing function with integer parameters for testing purposes.
"""
from __future__ import division, print_function, with_statement

from metaopt.core import param


@param.int("a", interval=(1, 10))
def f(a):
    """Function an integer parameter that fails, rising an exception."""
    del a
    raise Exception()
