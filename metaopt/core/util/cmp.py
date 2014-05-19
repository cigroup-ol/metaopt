# -*- coding: utf-8 -*-
"""
cmp built-in implementation for python 3.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


def cmp(a, b):
    """
    cmp built-in implementation for python 3.

    :param a: The first object to compare to a second.
    :param b: The second object to compare to a first.
    """
    return (a > b) - (a < b)
