# -!- coding: utf-8 -!-
from __future__ import division, print_function, with_statement

from orges.core.args import ArgsCreator
from orges.optimizer.base import BaseCaller, BaseOptimizer
from orges.util.stoppable import StoppedException


class GridSearchOptimizer(BaseOptimizer, BaseCaller):
    """TODO: Document"""

    def __init__(self):
        self.best = (None, None)

    @property
    def invoker(self):
        return self._invoker

    @invoker.setter
    def invoker(self, invoker):
        invoker.caller = self
        self._invoker = invoker

    def optimize(self, function, param_spec, return_spec=None):
        args_creator = ArgsCreator(param_spec)

        for args in args_creator.product():
            try:
                self._invoker.invoke(function, args)
            except StoppedException:
                return self.best[0]

        self._invoker.wait()

        return self.best[0]

    def on_result(self, fitness, args, *vargs):
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (args, fitness)

    def on_error(self, error, args, **kwargs):
        pass
