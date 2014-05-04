"""
Worker implementation that executes objective functions in Python threads.
"""
from threading import Thread
from metaopt.worker.worker import Worker


class ThreadWorker(Thread, Worker):
    """
    Worker implementation that executes objective functions in Python threads.
    """

    def __init__(self):
        pass
