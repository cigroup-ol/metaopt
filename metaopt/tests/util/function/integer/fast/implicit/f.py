"""
A working function with integer parameters for testing purposes.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core import param


@param.int("a", interval=(0, 1))
def f(a):
    """Function with one parameter."""
    return a
