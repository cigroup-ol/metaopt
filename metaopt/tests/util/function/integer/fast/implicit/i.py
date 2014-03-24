"""
A working function with integer parameters for testing purposes.
"""
from __future__ import division, print_function, with_statement

from metaopt.core import param


@param.int("a", interval=(1, 4))
@param.int("b", interval=(1, 2))
def f(a, b):
    """Function with two overlapping integer ranges."""
    return -(a + b)
