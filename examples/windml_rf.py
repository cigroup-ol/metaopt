# -*- coding: utf-8 -*-
"""
Random Forest for Wind Power Prediction (SAES, global timeout)
================================
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
#from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
import math

# First Party
from metaopt.core.param.util import param
from metaopt.core.returns.util.decorator import maximize

feature_window, horizon = 3, 3 
train_step, test_step = 100,100 #only every n data points
park_id=NREL.park_id['lancaster']
windpark = NREL().get_windpark_nearest(park_id, 10, 2004, 2005)
target = windpark.get_target()
mapping = PowerMapping()
X = mapping.get_features_park(windpark, feature_window, horizon)
y = mapping.get_labels_turbine(target, feature_window, horizon)
train_to, test_to = int(math.floor(len(X) * 0.5)), len(X)
X_train=X[:train_to:train_step]
y_train=y[:train_to:train_step]
X_test=X[train_to:test_to:test_step]
y_test=y[train_to:test_to:test_step]






@maximize("Score")
#@param.float("C", interval=[1, 1000], step=1.0)
#@param.float("C_exp", interval=[0, 5], step=1)
#@param.float("gamma", interval=[0.0001, 1.0], step=0.00001)
#@param.float("gamma_exp", interval=[-5, 0], step=1)
@param.int("N",interval=[1,50],step=1)
@param.int("M",interval=[1,10],step=1)
def f(N,M):
    clf = RandomForestRegressor(n_estimators=N,max_features=M, n_jobs=1) 
    #clf = AdaBoostRegressor(n_estimators=N,max_features=M) 

    clf.fit(X_train, y_train)

    return clf.score(X_test, y_test)


def main():
    from metaopt.core.main import optimize
    from metaopt.core.main import custom_optimize
    from metaopt.optimizer.saes import SAESOptimizer
    from metaopt.optimizer.gridsearch import GridSearchOptimizer

    from metaopt.invoker.dualthread import DualThreadInvoker
    from metaopt.invoker.pluggable import PluggableInvoker

    from metaopt.plugins.print import PrintPlugin
    from metaopt.plugins.visualize import VisualizeLandscapePlugin
    from metaopt.plugins.visualize import VisualizeBestFitnessPlugin

    timeout = 30 
    optimizer = SAESOptimizer(mu=5, lamb=5)
    #optimizer = GridSearchOptimizer()

    visualize_landscape_plugin = VisualizeLandscapePlugin()
    visualize_best_fitness_plugin = VisualizeBestFitnessPlugin()

    plugins = [
        PrintPlugin(),
        visualize_landscape_plugin,
        visualize_best_fitness_plugin
    ]


    #invoker = PluggableInvoker(invoker=DualThreadInvoker(),plugins=plugins)

    #optimum = custom_optimize(invoker=invoker,f=f, timeout=timeout, optimizer=optimizer)



    optimum = optimize(f=f, timeout=timeout, optimizer=optimizer,
                       plugins=plugins)

    print("The optimal parameters are %s." % str(optimum))

#    visualize_landscape_plugin.show_surface_plot()
#    visualize_landscape_plugin.show_image_plot()
#
    visualize_best_fitness_plugin.show_fitness_invocations_plot()
#    visualize_best_fitness_plugin.show_fitness_time_plot()

if __name__ == '__main__':
    main()
