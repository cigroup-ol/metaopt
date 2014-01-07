"""Collection of functions with integer parameters for testing purposes."""
from __future__ import division, print_function, with_statement

from time import sleep

from orges.core import param


@param.int("a", interval=(0, 1))
def f(a):
    """Function with one parameter."""
    return a


@param.int("a", interval=(0, 1))
def g(a):
    """Function with one parameter and a delayed negated result."""
    sleep(2)
    return -a


@param.int("a", interval=(1, 2))
@param.int("b", interval=(3, 4))
def h(a, b):
    """Function with two non-overlapping integer ranges."""
    return -(a + b)


@param.int("a", interval=(1, 4))
@param.int("b", interval=(2, 3))
def i(a, b):
    """Function with an integer range containing the other."""
    return -(a + b)


@param.int("a", interval=(1, 4))
@param.int("b", interval=(1, 2))
def j(a, b):
    """Function with two overlapping integer ranges."""
    return -(a + b)


@param.int("a", interval=(0, 4))
@param.int("b", interval=(0, 2))
def k(a, b):
    """Function with two integer ranges starting at 0."""
    return -(a + b)


@param.int("a", interval=(0, 1))
@param.int("b", interval=(1, 2))
def l(a, b):
    """Function with two integer ranges of length 1."""
    return -(a + b)

INTEGER_FUNCTIONS = [f, g, h, i, j, k, l]
