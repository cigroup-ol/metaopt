# -*- coding: utf-8 -*-
"""
A failing function with integer parameters for testing purposes.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util import param


@param.int("a", interval=(1, 10))
@param.int("b", interval=(1, 10))
def f(a, b):
    """Function with two integer parameters that fails, rising an exception."""
    del a, b
    raise Exception()
