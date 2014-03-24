"""
A failing function with integer parameters for testing purposes.
"""
from __future__ import division, print_function, with_statement

from time import sleep

from metaopt.core import param


@param.int("a", interval=(1, 10))
@param.int("b", interval=(1, 10))
def f(a, b):
    """Function that takes a long time to finish."""
    del a, b
    sleep(3600)
