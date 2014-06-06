"""
Optimzing the OneMin objective function with grid search
========================================================

The optimization stops after a global timeout of 10 seconds.

"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.optimize.optimize import optimize
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import minimize
from metaopt.optimizer.gridsearch import GridSearchOptimizer
from metaopt.optimizer.saes import SAESOptimizer
from metaopt.plugin.print.optimum import OptimumPrintPlugin
from metaopt.plugin.print.status import StatusPrintPlugin
from metaopt.plugin.visualization.best_fitness import VisualizeBestFitnessPlugin

@minimize("Sum")
@param.multi(param.bool, map(str, range(16)))
def f(**kwargs):
    return sum(kwargs.values())

def main():
    optimizer = GridSearchOptimizer()
    timeout = 10

    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        OptimumPrintPlugin(),
        visualize_best_fitness_plugin,
    ]

    optimum = optimize(f, timeout=timeout, optimizer=optimizer, plugins=plugins)

    print("The optimal parameters are %s." % str(optimum))

    visualize_best_fitness_plugin.show_fitness_invocations_plot()
    visualize_best_fitness_plugin.show_fitness_time_plot()

if __name__ == '__main__':
    main()
