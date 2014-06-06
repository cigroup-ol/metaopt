#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test function for KNN regression feature importance
=====================================================================
We generate test data for KNN regression. The goal is to provide a data
set, which has relevant and irrelevant features for regression. We use
a Friedman #1 problem and add zeros and random data.
We optimize the selection of features with an SAES.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First party
from metaopt.core.returnspec.util.decorator import minimize
from metaopt.core.paramspec.util import param
from metaopt.core.optimize.optimize import optimize



# Third Party
from sklearn.datasets import make_friedman1
from sklearn.neighbors import KNeighborsRegressor
from sklearn.base import BaseEstimator 
from sklearn.base import RegressorMixin
from sklearn.metrics import mean_squared_error as mse
import numpy as np
import math

class KNN(BaseEstimator, RegressorMixin):
    """
    K Nearest Neighbors Regression with feature filter 
    """
    def __init__(self, n_neighbors=5, ff=[True,True,True,True]):
        """
        :param n_neighbors: number of nearest neighbors searched
        :param ff: feature filter 
        """
        self.n_neighbors=n_neighbors
        self.ff = np.array(ff,dtype=bool)
        self.knn=KNeighborsRegressor(n_neighbors=self.n_neighbors)

    def fit(self,X,y):
        # Choose the selected features
        self.knn.fit(X[:,self.ff], y)

    def predict(self,X):
        # Choose the selected features
        return self.knn.predict(X[:,self.ff])

    def score(self,X,y):
        # Choose the selected features
        return mse(self.knn.predict(X[:,self.ff]),y)


n_samples=1000
n_informative=5
n_zeros=5
n_random=5
n_features=n_informative+n_zeros+n_random

# Generate a regression problem data set
# Inputs X are independent features uniformly distributed on the interval [0, 1]. The output y is created according to the formula:
# y(X) = 10 * sin(pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 + 10 * X[:, 3] + 5 * X[:, 4] + noise * N(0, 1).
X,Y = make_friedman1(n_samples=n_samples, n_features=n_informative, noise=0.0, random_state=13)
X=np.array(X)

# Fill up the data with zeros 
Z1=np.zeros((n_samples, n_zeros))
X=np.hstack((X,Z1))

# Fill up the data with random 
Z2=np.random.random((n_samples, n_random))
X=np.hstack((X,Z2))

train_to, test_to = int(math.floor(len(X) * 0.5)), len(X)
X_train=X[:train_to:1]
y_train=Y[:train_to:1]
X_test=X[train_to:test_to:1]
y_test=Y[train_to:test_to:1]

"""
Evaluate the KNN regression using the featrue filter ff
"""
@minimize("KNN Regression MSE")
@param.multi(param.bool, map(str,range(n_features)))
def f(**kwargs):
    """
    :param ff: feature filter 
    """
    clf = KNN(n_neighbors=5, ff=kwargs.values())
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)

def main():
    from metaopt.optimizer.saes import SAESOptimizer
    from metaopt.concurrent.invoker.dualthread import DualThreadInvoker
    from metaopt.concurrent.invoker.pluggable import PluggableInvoker
    from metaopt.plugin.print.status import StatusPrintPlugin
    from metaopt.plugin.visualization.landscape import VisualizeLandscapePlugin
    from metaopt.plugin.visualization.best_fitness import VisualizeBestFitnessPlugin

    timeout = 10 
    optimizer = SAESOptimizer(mu=5, lamb=5)

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        visualize_best_fitness_plugin
    ]
    optimum = optimize(f=f, timeout=timeout, optimizer=optimizer,
                       plugins=plugins)

    print("The optimal parameters are %s." % str(optimum))

    visualize_best_fitness_plugin.show_fitness_invocations_plot()
    visualize_best_fitness_plugin.show_fitness_time_plot()



if __name__ == '__main__':
    main()
