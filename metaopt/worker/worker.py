"""
Minimal worker implementation.
"""
from __future__ import division, print_function, with_statement

from metaopt.worker.base import BaseWorker


class Worker(BaseWorker):
    """Minimal worker implementation."""

    def __init__(self):
        super(Worker, self).__init__()
        self._worker_id = None

    @property
    def worker_id(self):
        return self._worker_id

    def run(self):
        raise NotImplementedError()
