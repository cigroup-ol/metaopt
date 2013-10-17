"""Runs an imported f() with the queue message as an argument."""

from __future__ import division
from __future__ import print_function

from orges.test.unit.hang import hang
from orges.demo.worker.payload_function_builder import get_worker_function


def worker(index, queue_tasks, queue_results):
    """Gets a worker function for hang from the builder and calls it."""
    worker_f = get_worker_function(hang)
    worker_f(index, queue_tasks, queue_results)
