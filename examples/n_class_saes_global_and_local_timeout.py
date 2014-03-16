# -*- coding: utf-8 -*-
"""
SVM (SAES, global timeout)
================================
"""
from __future__ import division, print_function, with_statement

from sklearn import cross_validation, datasets, svm

from metaopt.core import param
from metaopt.core.returns import maximize


@maximize("Score")
@param.float("C", interval=[1, 10], step=0.5)
@param.float("gamma", interval=[1, 10], step=0.5)
def f(C, gamma):
    X, y = datasets.make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=2,
        n_classes=2,
        n_clusters_per_class=1,
        random_state=0
    )

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        X, y, test_size=0.4, random_state=0)

    clf = svm.SVC(C=C, gamma=gamma)

    clf.fit(X_train, y_train)

    return clf.score(X_test, y_test)


def main():
    from metaopt.core.main import optimize
    from metaopt.optimizer.saes import SAESOptimizer

    from metaopt.plugins.print import PrintPlugin
    from metaopt.plugins.visualize import VisualizeLandscapePlugin
    from metaopt.plugins.visualize import VisualizeBestFitnessPlugin
    from metaopt.plugins.timeout import TimeoutPlugin

    optimizer = SAESOptimizer()

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        PrintPlugin(),
        visualize_landscape_plugin,
        visualize_best_fitness_plugin,
        TimeoutPlugin(2),
    ]

    print(optimize(f, timeout=10, optimizer=optimizer, plugins=plugins))

    visualize_landscape_plugin.show_surface_plot()
    visualize_landscape_plugin.show_image_plot()

    visualize_best_fitness_plugin.show_fitness_invocations_plot()
    visualize_best_fitness_plugin.show_fitness_time_plot()

if __name__ == '__main__':
    main()
