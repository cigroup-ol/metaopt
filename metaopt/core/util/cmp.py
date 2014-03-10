"""
cmp built-in implementation for python 3.
"""
from __future__ import division, print_function, with_statement


def cmp(a, b):
    """cmp built-in implementation for python 3."""
    return (a > b) - (a < b)
