"""Collection of no-self-use methods to build a Manager from."""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement


def kill_worker_by_id(worker_pool, id):
    """Terminates a worker from the given worker pool given by id."""
    worker = worker_pool.workers[0]
    kill_worker(worker)


def kill_worker(worker):
    """Kills the given worker."""
    worker.process.terminate()
