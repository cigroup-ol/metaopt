"""Runs an imported f() with the queue message as an argument."""

from __future__ import division
from __future__ import print_function

from orges.test.demo.algorithm.host.saes import f
from orges.invoker.multiprocess_lib.worker.worker_builder import \
        get_worker_for_function


def get_worker():
    """Gets a worker function for hang from the builder and calls it."""
    return get_worker_for_function(f)
