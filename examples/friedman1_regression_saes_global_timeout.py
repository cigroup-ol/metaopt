# -*- coding: utf-8 -*-
"""
Optimization of KNN Distance Function Weights  (SAES, global timeout)
=====================================================================
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
from sklearn.metrics import mean_squared_error as mse
from sklearn.datasets import make_friedman1
import numpy as np
import math
import math
from metaopt.core.returnspec.util.decorator import minimize
from metaopt.core.paramspec.util import param
from metaopt.core.optimize.optimize import optimize


class KNN:
    """
    K Nearest Neighbros Regression with a custom distance metric.
    The distance function uses the given weights for the particular features.    
    """
    def __init__(self, n_neighbors=5, weights=[1.0,1.0,1.0,1.0]):
        """
        :param n_neighbors: number of nearest neighbors searched
        :param weights: weights for distance metric
        """
        self.n_neighbors=n_neighbors
        self.weights=weights

    def fit(self,X,y):
        """
        :param X: Training patterns
        :param y: Training labels
        """
        self.X_train = X
        self.y_train = y

    def dist(self, A,B):
        assert(len(A) == len(B) == len(self.weights))
        l = len(B)
        sum=0.0
        denom=0.0
        for i in range(l):
            sum += (float(A[i])-float(B[i]))**2 * float(self.weights[i])
            denom += float(self.weights[i])
        assert(denom!=0)
        sum /= denom
        return sum

    def predict(self,X):
        res=[]
        for q in X:
            D=[] # list of distances to the train instances
            for t in self.X_train:
                D.append(self.dist(q,t))

            neighbor_labels=self.y_train[np.argsort(D)][0:self.n_neighbors]
            avg = np.mean(neighbor_labels)
            res.append(avg)
        return res

    def score(self,X,y):
        res = self.predict(X)
        return math.sqrt(mse(res,y))

# Generate a Friedman #1 Problem
X,Y = make_friedman1(n_samples=300, n_features=10, noise=0.0, random_state=13)
train_to, test_to = int(math.floor(len(X) * 0.5)), len(X)
X_train=X[:train_to:1]
y_train=Y[:train_to:1]
X_test=X[train_to:test_to:1]
y_test=Y[train_to:test_to:1]

@minimize("Score")
@param.multi(param.float, map(str,range(10)), interval=[1.0,100.0])

def f(**kwargs):
    clf = KNN(n_neighbors=5, weights=kwargs.values())
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)


def main():
    from metaopt.optimizer.saes import SAESOptimizer
    from metaopt.optimizer.rechenberg import RechenbergOptimizer

    from metaopt.concurrent.invoker.dualthread import DualThreadInvoker
    from metaopt.concurrent.invoker.pluggable import PluggableInvoker

    from metaopt.plugin.print.status import StatusPrintPlugin
    from metaopt.plugin.visualization.landscape import VisualizeLandscapePlugin
    from metaopt.plugin.visualization.best_fitness import VisualizeBestFitnessPlugin

    timeout = 5
    optimizer = SAESOptimizer(mu=5, lamb=5)

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        #StatusPrintPlugin(),
        visualize_landscape_plugin,
        visualize_best_fitness_plugin
    ]
    optimum = optimize(f=f, timeout=timeout, optimizer=optimizer,
                       plugins=plugins)

    print("The optimal parameters are %s." % str(optimum))

    visualize_best_fitness_plugin.show_fitness_invocations_plot()

if __name__ == '__main__':
    main()
