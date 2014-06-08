# -*- coding: utf-8 -*-
"""
Optimizing the parameters of a SVM applied to the Iris data set
===============================================================

The parameters are optimized with grid search. Optimization stops after a global
timeout of 10 seconds.

"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
from sklearn import cross_validation, datasets, svm

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import maximize


@maximize("Score")
@param.float("C-Exp", interval=[0, 4], step=0.1)
@param.float("Gamma-Exp", interval=[-6, 0], step=0.1)
def f(C_exp, gamma_exp):
    iris = datasets.load_iris()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        iris.data, iris.target, test_size=0.4, random_state=0)

    C = 10 ** C_exp
    gamma = 10 ** gamma_exp

    clf = svm.SVC(C=C, gamma=gamma)

    clf.fit(X_train, y_train)

    return clf.score(X_test, y_test)


def main():
    from metaopt.core.optimize.optimize import optimize
    from metaopt.optimizer.gridsearch import GridSearchOptimizer

    from metaopt.plugin.print.optimum import OptimumPrintPlugin
    from metaopt.plugin.timeout import TimeoutPlugin

    from metaopt.plugin.visualization.best_fitness \
        import VisualizeBestFitnessPlugin

    from metaopt.plugin.visualization.landscape import VisualizeLandscapePlugin

    timeout = 10
    optimizer = GridSearchOptimizer()

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        OptimumPrintPlugin(),
        visualize_landscape_plugin,
        visualize_best_fitness_plugin,
    ]

    optimum = optimize(f, timeout=timeout, optimizer=optimizer, plugins=plugins)

    print("The optimal parameters are %s." % str(optimum))

    visualize_landscape_plugin.show_surface_plot()
    visualize_landscape_plugin.show_image_plot()

    visualize_best_fitness_plugin.show_fitness_invocations_plot()
    visualize_best_fitness_plugin.show_fitness_time_plot()

if __name__ == '__main__':
    main()
