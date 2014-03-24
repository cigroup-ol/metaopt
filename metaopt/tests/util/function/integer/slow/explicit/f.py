"""
Hanging function with integer parameters and explicit maximization.
"""
from __future__ import division, print_function, with_statement

from time import sleep

from metaopt.core import param
from metaopt.core.returns import maximize


@maximize("y")
@param.int("x", interval=[0, 10])
def f(x):
    sleep(1)
    return x
