"""Runs an imported f() with the queue message as an argument."""

from __future__ import division, print_function, with_statement

from examples.algorithm.hang import hang


def get_worker():
    """Gets a get_worker function for hang from the builder and returns it."""
    return hang
