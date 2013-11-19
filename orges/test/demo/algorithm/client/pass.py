"""
Worker that returns nothing.
"""

from __future__ import division, print_function, with_statement


def _pass_function():
    """Function that returns nothing."""
    pass


def get_worker():
    """Gets a get_worker function for hang from the builder and returns it."""
    return _pass_function
