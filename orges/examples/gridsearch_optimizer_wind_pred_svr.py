# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

import math

from sklearn.svm import SVR


# to run this example, add windml, branch 'develop' to your PYTHONPATH
# https://github.com/cigroup-ol/windml.git
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping

from orges.plugins.print import PrintPlugin
from orges.main import optimize
from orges.optimizer.singleinvoke import SingleInvokeOptimizer
import orges.param as param


@param.int("C_exp", interval=(1, 10), display_name="C_exp")
@param.int("neg_gamma_exp", interval=(2, 15), display_name="gamma_exp")
def f(C_exp, neg_gamma_exp):
    gamma_exp = -(neg_gamma_exp)

    park_id = NREL.park_id['tehachapi']
    windpark = NREL().get_windpark(park_id, 3, 2004, 2005)
    target = windpark.get_target()

    # use power mapping for pattern-label mapping. Feature window length is 3 time
    # steps and time horizon (forecast) is 3 time steps.
    feature_window = 3
    horizon = 3
    mapping = PowerMapping()
    X = mapping.get_features_park(windpark, feature_window, horizon)
    Y = mapping.get_labels_turbine(target, feature_window, horizon)

    # train roughly for the year 2004.
    train_to = int(math.floor(len(X) * 0.5))

    # test roughly for the year 2005.
    test_to = len(X)

    # train and test only every fifth pattern, for performance.
    train_step, test_step = 5, 5

    # train a SVR regressor with best found parameters.
    svr = SVR(kernel='rbf', epsilon=0.1, C = 2**C_exp,\
        gamma = 2**gamma_exp)

    # fitting the pattern-label pairs
    svr.fit(X[0:train_to:train_step], Y[0:train_to:train_step])

    y_hat = svr.predict(X[train_to:test_to:test_step])

    mse_y_hat, mse_naive_hat = 0, 0
    for i in range(0, len(y_hat)):
        y = Y[train_to + (i * test_step)]
        mse_y_hat += (y_hat[i] - y) ** 2

    mse_y_hat /= float(len(y_hat))

    return mse_y_hat

if __name__ == '__main__':
    plugins = [PrintPlugin()]

    print(optimize(function=f, optimizer=SingleInvokeOptimizer(),
                   plugins=plugins))
