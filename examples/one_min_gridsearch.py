"""
One Min (grid search)
=====================
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.param.util import param
from metaopt.core.returns.util.decorator import minimize
from metaopt.plugin.print.optimum import OptimumPrintPlugin


@minimize("value")
@param.bool("a")
@param.bool("b")
@param.bool("c")
@param.bool("d")
@param.bool("e")
@param.bool("f")
@param.bool("g")
@param.bool("h")
def f(**kwargs):
    return sum(kwargs.values())


def main():
    from metaopt.core.main import optimize
    from metaopt.optimizer.gridsearch import GridSearchOptimizer

    from metaopt.plugin.print.status import StatusPrintPlugin
    from metaopt.plugin.visualization.landscape import VisualizeLandscapePlugin
    from metaopt.plugin.visualization.best_fitness import \
        VisualizeBestFitnessPlugin

    optimizer = GridSearchOptimizer()

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

    optimize(f=f, optimizer=optimizer, plugins=plugins)

    visualize_landscape_plugin.show_surface_plot()
    visualize_landscape_plugin.show_image_plot()

    visualize_best_fitness_plugin.show_fitness_invocations_plot()
    visualize_best_fitness_plugin.show_fitness_time_plot()

if __name__ == '__main__':
    main()
