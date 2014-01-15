# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

from sklearn import svm, datasets, cross_validation

from orges.core import param


@param.float("C", interval=[0.1, 2])
@param.float("gamma", interval=[0, 2])
def f(C, gamma):
    iris = datasets.load_iris()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        iris.data, iris.target, test_size=0.4, random_state=0)

    clf = svm.SVC(C=C, gamma=gamma)

    clf.fit(X_train, y_train)

    return -clf.score(X_test, y_test)


if __name__ == '__main__':
    from orges.core.main import optimize
    from orges.optimizer.saes import SAESOptimizer

    from orges.plugins.print import PrintPlugin
    from orges.plugins.visualize import VisualizeLandscapePlugin
    from orges.plugins.visualize import VisualizeBestFitnessPlugin

    optimizer = SAESOptimizer()

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        PrintPlugin(),
        visualize_landscape_plugin,
        visualize_best_fitness_plugin
    ]

    print(optimize(f, timeout=1, optimizer=optimizer, plugins=plugins))

    visualize_landscape_plugin.save_visualization()
    visualize_best_fitness_plugin.save_visualization()
