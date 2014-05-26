"""
One Min (grid search)
=====================

This example uses an objective function included in MetaOpt. For it's
implementation see `metaopt.objective.bool.one_min_eight`.
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
from metaopt.plugin.visualization.landscape import VisualizeLandscapePlugin

@minimize("Sum")
@param.multi(param.bool, ["a", "b", "c", "d", "e", "f", "g", "h"])
def f(**kwargs):
    return sum(kwargs.values())

def main():
    optimizer = SAESOptimizer(mu=1000,lamb=1000)

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()
    status_print_plugin = StatusPrintPlugin()
    optimum_print_plugin = OptimumPrintPlugin()

    plugins = [
        status_print_plugin,
        optimum_print_plugin,
        visualize_landscape_plugin,
        visualize_best_fitness_plugin
    ]

    optimize(f=f, timeout=10, optimizer=optimizer, plugins=plugins)

    visualize_landscape_plugin.show_surface_plot()
    visualize_landscape_plugin.show_image_plot()

    visualize_best_fitness_plugin.show_fitness_invocations_plot()
    visualize_best_fitness_plugin.show_fitness_time_plot()

if __name__ == '__main__':
    main()
