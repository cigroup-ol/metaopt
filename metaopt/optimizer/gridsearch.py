# -!- coding: utf-8 -!-
from __future__ import division, print_function, with_statement

from metaopt.core.args import ArgsCreator
from metaopt.optimizer.base import BaseCaller, BaseOptimizer
from metaopt.util.stoppable import StoppedException


class GridSearchOptimizer(BaseOptimizer, BaseCaller):
    """TODO: Document me"""

    def __init__(self):
        self.best = (None, None)

    def optimize(self, invoker, param_spec, return_spec=None):
        args_creator = ArgsCreator(param_spec)

        for args in args_creator.product():
            try:
                invoker.invoke(self, args)
            except StoppedException:
                return self.best[0]

        invoker.wait()

        return self.best[0]

    def on_result(self, fitness, args, **kwargs):
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (args, fitness)

    def on_error(self, error, args, **kwargs):
        pass
