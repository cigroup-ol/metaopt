"""Runs an imported f() with the queue message as an argument."""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from orges.test.unit.hang import hang


def get_worker():
    """Gets a get_worker function for hang from the builder and returns it."""
    return hang
