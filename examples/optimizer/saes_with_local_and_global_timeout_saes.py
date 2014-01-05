# -*- coding: utf-8 -*-
"""
Example demonstrating the SAES optimizer with local and global timeout.
"""
from __future__ import division, print_function, with_statement

import orges.core.param as param
from orges.core.main import optimize
from orges.plugins.print import PrintPlugin
from orges.optimizer.saes import SAESOptimizer
from orges.plugins.timeout import TimeoutPlugin
from examples.algorithm.saes import f as saes


@param.int("mu", interval=(5, 10), title="μ")
@param.int("lambd", interval=(5, 10), title="λ")
@param.float("tau0", interval=(0, 1), step=0.5, title="τ0")
@param.float("tau1", interval=(0, 1), step=0.5, title="τ1")
def f(mu, lambd, tau0, tau1):
    args = dict()

    args["d"] = 2
    args["epsilon"] = 0.0001
    args["mu"] = mu
    args["lambd"] = lambd
    args["tau0"] = tau0
    args["tau1"] = tau1

    return saes(args)

if __name__ == '__main__':
    LOCAL_TIMEOUT = 1  # Local timeout after 1 second
    GLOBAL_TIMEOUT = 5  # Global timeout after 5 seconds

    print(optimize(function=f, optimizer=SAESOptimizer(),
                   timeout=GLOBAL_TIMEOUT,
                   plugins=[TimeoutPlugin(LOCAL_TIMEOUT),
                            PrintPlugin()]))
