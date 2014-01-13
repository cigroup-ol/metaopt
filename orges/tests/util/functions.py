"""
Collection of functions of the function package for testing purposes.
"""
from __future__ import division, print_function, with_statement

from orges.tests.util.function.integer.failing.m import f as m
from orges.tests.util.function.integer.failing.n import f as n
from orges.tests.util.function.integer.working.f import f as f
from orges.tests.util.function.integer.working.g import f as g
from orges.tests.util.function.integer.working.h import f as h
from orges.tests.util.function.integer.working.i import f as i
from orges.tests.util.function.integer.working.j import f as j
from orges.tests.util.function.integer.working.k import f as k
from orges.tests.util.function.integer.working.l import f as l

FUNCTIONS_INTEGER_WORKING = [f, g, h, i, j, k, l]

FUNCTIONS_INTEGER_FAILING = [m, n]
