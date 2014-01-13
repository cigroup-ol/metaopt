"""
A working function with integer parameters for testing purposes.
"""
from __future__ import division, print_function, with_statement

from orges.core import param


@param.int("a", interval=(0, 4))
@param.int("b", interval=(0, 2))
def f(a, b):
    """Function with two integer ranges starting at 0."""
    return -(a + b)
