# -*- coding: utf-8 -*-
"""
SVM (Gridsearch, global timeout)
================================
"""
from __future__ import division, print_function, with_statement

from sklearn import cross_validation, datasets, svm

from metaopt.core import param
from metaopt.core.returns import maximize


@maximize("Score")
@param.float("C", interval=[1, 10], step=0.25)
@param.float("gamma", interval=[1, 10], step=0.25)
def f(C, gamma):
    iris = datasets.load_iris()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        iris.data, iris.target, test_size=0.4, random_state=0)

    clf = svm.SVC(C=C, gamma=gamma)

    clf.fit(X_train, y_train)

    return clf.score(X_test, y_test)


def main():
    from metaopt.core.main import optimize
    from metaopt.optimizer.gridsearch import GridSearchOptimizer

    from metaopt.plugins.print import PrintPlugin
    from metaopt.plugins.visualize import VisualizeLandscapePlugin
    from metaopt.plugins.visualize import VisualizeBestFitnessPlugin

    optimizer = GridSearchOptimizer()

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        PrintPlugin(),
        visualize_landscape_plugin,
        visualize_best_fitness_plugin
    ]

    print(optimize(f, timeout=3, optimizer=optimizer, plugins=plugins))

    visualize_landscape_plugin.show_surface_plot()
    visualize_landscape_plugin.show_image_plot()

    visualize_best_fitness_plugin.show_fitness_invocations_plot()
    visualize_best_fitness_plugin.show_fitness_time_plot()

if __name__ == '__main__':
    main()
