"""
Minimal caller implementation.
"""
from metaopt.optimizer.base import BaseCaller


class Caller(BaseCaller):
    """
    Minimal caller implementation.
    """

    def __init__(self):
        super(Caller, self).__init__()

    def on_result(self, value, fargs, **kwargs):
        raise NotImplementedError()

    def on_error(self, value, fargs, **kwargs):
        raise NotImplementedError()
