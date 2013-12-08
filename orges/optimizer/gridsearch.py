# -!- coding: utf-8 -!-
from __future__ import division, print_function, with_statement

from orges.args import ArgsCreator
from orges.optimizer.base import BaseCaller, BaseOptimizer


class GridSearchOptimizer(BaseOptimizer, BaseCaller):
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
            _, aborted = self._invoker.invoke(function, args)

            if aborted:
                return self.best[0]

        self._invoker.wait()

        return self.best[0]

    # Wird aufgerufen wenn ein Aufruf von f beendet wurde.
    def on_result(self, fitness, args, *vargs):
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (args, fitness)

    # Wird aufgerufen wenn beim Aufruf von f ein Fehler aufgetaucht ist.
    def on_error(self, args, **kwargs):
        pass
