#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minimize the Sum of Squares using SAES
=====================================================================
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

n_params=15

"""
Sum of squares
"""
@minimize("Sum")
@param.multi(param.float, map(str,range(n_params)),interval=[0, 5], step=1)
def f(**kwargs):
    sq=[v**2 for v in kwargs.values()]
    return sum(sq)

def main():
    from metaopt.optimizer.saes import SAESOptimizer
    from metaopt.concurrent.invoker.dualthread import DualThreadInvoker
    from metaopt.concurrent.invoker.pluggable import PluggableInvoker
    from metaopt.plugin.print.status import StatusPrintPlugin
    from metaopt.plugin.visualization.best_fitness import VisualizeBestFitnessPlugin

    timeout = 30 
    optimizer = SAESOptimizer(mu=5, lamb=5)
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        visualize_best_fitness_plugin
    ]
    optimum = optimize(f=f, timeout=timeout, optimizer=optimizer,
                       plugins=plugins)
    print("The optimal parameters are %s." % str(optimum))
    visualize_best_fitness_plugin.show_fitness_invocations_plot()

if __name__ == '__main__':
    main()
