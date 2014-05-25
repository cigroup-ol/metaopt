# -*- coding: utf-8 -*-
"""
Minimal worker implementation.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.concurrent.worker.base import BaseWorker


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
