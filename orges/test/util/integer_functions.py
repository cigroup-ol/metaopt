"""Functions with only integer parameters."""
from orges import param


@param.int("a", interval=(1, 2))
@param.int("b", interval=(3, 4))
def f(a, b):
    """Function with two non-overlapping integer ranges."""
    return -(a + b)


@param.int("a", interval=(1, 4))
@param.int("b", interval=(2, 3))
def g(a, b):
    """Function with an integer range containing the other."""
    return -(a + b)


@param.int("a", interval=(1, 4))
@param.int("b", interval=(1, 2))
def h(a, b):
    """Function with two overlapping integer ranges."""
    return -(a + b)


@param.int("a", interval=(0, 4))
@param.int("b", interval=(0, 2))
def i(a, b):
    """Function with two integer ranges starting at 0."""
    return -(a + b)


@param.int("a", interval=(0, 1))
@param.int("b", interval=(1, 2))
def j(a, b):
    """Function with two integer ranges of length 1."""
    return -(a + b)


INTEGER_FUNCTIONS = [f, g, h, i, j]
