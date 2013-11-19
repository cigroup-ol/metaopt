# -!- coding: utf-8 -!-
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from orges.args import ArgsCreator
from orges.optimizer.base import BaseOptimizer


class GridSearchOptimizer(BaseOptimizer):
    # Invoker ist erstmal ein Objekt, mit dem man Prozesse aufrufen kann
    def __init__(self):
        self.best = (None, None)

    @property
    def invoker(self):
        return self._invoker

    @invoker.setter
    def invoker(self, invoker):
        invoker.caller = self
        self._invoker = invoker

    def optimize(self, f_package, param_spec, return_spec=None, minimize=True):
        args_creator = ArgsCreator(param_spec)

        for args in args_creator.product():
            #print("calling invoke")
            _, aborted = self._invoker.invoke(f_package, args)
            #print("called invoke", _, aborted)

            if aborted:
                return self.best

        self._invoker.wait()

        return self.best

    # Wird aufgerufen wenn ein Aufruf von f beendet wurde.
    def on_result(self, result, args, *vargs):
        # solution, fitness = result
        fitness = result
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (args, fitness)

    # Wird aufgerufen wenn beim Aufruf von f ein Fehler aufgetaucht ist.
    def on_error(self, args, **kwargs):
        pass
