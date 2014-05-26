# -*- coding: utf-8 -*-
"""
Interface definition for worker implementations.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from abc import ABCMeta, abstractmethod


class BaseWorker(object):
    """Interface definition for worker implementations."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        super(BaseWorker, self).__init__()

    @abstractmethod
    def worker_id(self):
        """Property for the _worker_id attribute."""
        pass

    @abstractmethod
    def run(self):
        """
        Makes this worker idle and pick up tasks from the  queue.
        """
        pass
