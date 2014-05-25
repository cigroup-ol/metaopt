# -*- coding: utf-8 -*-
"""
A failing function with integer parameters for testing purposes.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from time import sleep

# First Party
from metaopt.core.paramspec.util import param


@param.int("a", interval=(1, 10))
@param.int("b", interval=(1, 10))
def f(a, b):
    """Function that takes a long time to finish."""
    del a, b
    sleep(3600)
