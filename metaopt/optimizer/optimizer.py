"""
Minimal optimizer implementation.
"""
from metaopt.optimizer.base import BaseOptimizer


class Optimizer(BaseOptimizer):
    """
    Minimal optimizer implementation.
    """

    def __init__(self):
        super(Optimizer, self).__init__()

    def on_result(self, value, fargs, **kwargs):
        raise NotImplementedError()

    def on_error(self, value, fargs, **kwargs):
        raise NotImplementedError()

    def optimize(self, invoker, param_spec, return_spec):
        raise NotImplementedError()
