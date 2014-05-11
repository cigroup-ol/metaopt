"""
Hanging function with integer parameters and explicit maximization.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from time import sleep

# First Party
from metaopt.core import param
from metaopt.core.returns import maximize


@maximize("y")
@param.int("x", interval=[0, 10])
def f(x):
    sleep(0.1)
    return x
