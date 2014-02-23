"""
A working function with integer parameters for testing purposes.
"""
from __future__ import division, print_function, with_statement

from metaopt.core import param


@param.int("a", interval=(0, 1))
def f(a):
    """Function with one parameter."""
    return a
