"""
A working function with integer parameters for testing purposes.
"""
from __future__ import division, print_function, with_statement

from orges.core import param


@param.int("a", interval=(1, 4))
@param.int("b", interval=(2, 3))
def f(a, b):
    """Function with an integer range containing the other."""
    return -(a + b)
