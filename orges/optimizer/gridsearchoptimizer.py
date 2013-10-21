# -*- coding: utf-8 -*-
from orges.framework.args import ArgsCreator

class GridSearchOptimizer(object):
    # Invoker ist erstmal ein Objekt, mit dem man Prozesse aufrufen kann
    def __init__(self, invoker):
        self.best = (None, None)

        self.invoker = invoker
        self.invoker.caller = self

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
    def on_result(self, args, result):
        # solution, fitness = result
        fitness = result
        _, best_fitness = self.best

        if best_fitness is None or fitness < best_fitness:
            self.best = (args, fitness)

    # Wird aufgerufen wenn beim Aufruf von f ein Fehler aufgetaucht ist.
    def on_error(args, error):
        return False # Bei True könnte man z.B. den Aufruf von F erneut probieren.