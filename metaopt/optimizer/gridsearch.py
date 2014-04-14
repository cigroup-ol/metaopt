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
        del return_spec  # TODO implement me
        args_creator = ArgsCreator(param_spec)

        for args in args_creator.product():
            try:
                invoker.invoke(caller=self, fargs=args)
            except StoppedException:
                return self.best[0]

        invoker.wait()

        return self.best[0]

    def on_result(self, value, fargs, **kwargs):
        fitness = value
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (fargs, fitness)

    def on_error(self, error, fargs, **kwargs):
        pass
