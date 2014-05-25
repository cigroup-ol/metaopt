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
def f(a):
    """Function an integer parameter that fails, rising an exception."""
    del a
    raise Exception()
