# -!- coding: utf-8 -!-

from orges.args import ArgsCreator

class GridSearchOptimizer(object):
    # Invoker ist erstmal ein Objekt, mit dem man Prozesse aufrufen kann
    def __init__(self, invoker):
        self.best = (None, None)
        self.invoker = invoker

    def optimize(self, f, param_spec, return_spec=None, minimize=True):
        args_creator = ArgsCreator(param_spec)

        for args in args_creator.product():
            # Wartet bis ein Prozess zur Verfügung steht, in dem f aufgerufen werden kann.
            self.invoker.call(f, args)
            yield self.best[0]

        # Wartet bis alle Aufrufe von f beendet sind.
        self.invoker.wait()

        yield self.best[0]

    # Wird aufgerufen wenn ein Aufruf von f beendet wurde.
    def on_result(self, args, result):
        solution, fitness = result
        _, best_fitness = self.best

        if fitness < best_fitness:
            self.best = (args, fitness)

    # Wird aufgerufen wenn beim Aufruf von f ein Fehler aufgetaucht ist.
    def on_error(self, args, error):
        return False # Bei True könnte man z.B. den Aufruf von F erneut probieren.
