# -*- coding: utf-8 -*-
"""
Working function with integer parameters and explicit maximization.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import minimize


@minimize("y")
@param.int("x", interval=[0, 10])
def f(x):
    return x
