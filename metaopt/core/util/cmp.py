"""
cmp built-in implementation for python 3.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


def cmp(a, b):
    """cmp built-in implementation for python 3."""
    return (a > b) - (a < b)
