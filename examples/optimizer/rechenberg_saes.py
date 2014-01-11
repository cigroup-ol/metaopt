# -*- coding: utf-8 -*-
"""
Example demonstrating an SAES target algorithm and the rechenberg optimizer.
"""
from __future__ import division, print_function, with_statement

import orges.core.param as param
from orges.core.main import optimize
from orges.plugins.print import PrintPlugin
from examples.algorithm.saes import f as saes
from orges.optimizer.rechenberg import RechenbergOptimizer


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
    print(optimize(f, optimizer=RechenbergOptimizer(),
                   plugins=[PrintPlugin()]))
