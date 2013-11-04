"""Runs an imported f() with the queue message as an argument."""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from orges.test.demo.algorithm.host.saes import f


def get_worker():
    """Gets a worker function for hang from the builder and calls it."""
    return f
