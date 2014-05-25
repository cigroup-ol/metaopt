# -*- coding: utf-8 -*-
"""
A working function with integer parameters for testing purposes.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util import param


@param.int("a", interval=(0, 4))
@param.int("b", interval=(0, 2))
def f(a, b):
    """Function with two integer ranges starting at 0."""
    return -(a + b)
