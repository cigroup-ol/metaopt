# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.stoppable.util.exception import StoppedError
from metaopt.optimizer.optimizer import Optimizer


class RandomSearchOptimizer(Optimizer):
    """Optimizer that systematically tests parameters in a grid pattern."""

    def __init__(self):
        super(RandomSearchOptimizer, self).__init__()
        self.best = (None, None)

    def optimize(self, invoker, param_spec, return_spec=None):
        args_creator = ArgsCreator(param_spec)

        try:
            while True:
                args = args_creator.random()
                invoker.invoke(self, args)
        except StoppedError:
            return self.best[0]

    def on_result(self, value, fargs, **kwargs):
        del kwargs
        fitness = value
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (fargs, fitness)

    def on_error(self, value, fargs, **kwargs):
        pass
