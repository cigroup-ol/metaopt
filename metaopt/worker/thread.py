# -*- coding: utf-8 -*-
"""
Worker implementation that executes objective functions in Python threads.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from threading import Thread

# First Party
from metaopt.worker.worker import Worker


class ThreadWorker(Thread, Worker):
    """
    Worker implementation that executes objective functions in Python threads.
    """

    def __init__(self):
        pass
