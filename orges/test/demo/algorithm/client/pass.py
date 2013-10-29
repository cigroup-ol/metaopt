"""
Worker that returns nothing.
"""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from orges.invoker.multiprocess_lib.worker.worker_builder import \
    get_worker_for_function


def _pass_function():
    """Function that returns nothing."""
    pass


def get_worker():
    """Gets a get_worker function for hang from the builder and returns it."""
    return get_worker_for_function(_pass_function)
