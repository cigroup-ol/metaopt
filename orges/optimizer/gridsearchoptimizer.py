# -!- coding: utf-8 -!-
from orges.args import ArgsCreator
from orges.optimizer.optimizer import Optimizer


class GridSearchOptimizer(Optimizer):
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

    def optimize(self, f, param_spec, return_spec=None, minimize=True):
        args_creator = ArgsCreator(param_spec)

        for args in args_creator.product():
            # Wartet bis ein Prozess zur Verfügung steht, in dem f aufgerufen werden kann.
            self.invoker.invoke(f, args)
            # yield self.best[0]

        # Wartet bis alle Aufrufe von f beendet sind.
        self.invoker.wait()

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
