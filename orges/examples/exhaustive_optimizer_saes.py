# -*- coding: utf-8 -*-
from orges.test.demo.algorithm.host.saes import f as saes

from orges.optimizer.gridsearchoptimizer import GridSearchOptimizer
from orges.optimizer.saesoptimizer import SAESOptimizer

from orges.main import optimize

import orges.param as param

@param.int("mu", interval=(5, 10), display_name="μ")
@param.int("lambd", interval=(5, 10), display_name="λ")
@param.float("tau0", interval=(0, 1), step=0.5, display_name="τ0")
@param.float("tau1", interval=(0, 1), step=0.5, display_name="τ1")
def f(mu, lambd, tau0, tau1):
    pass

if __name__ == '__main__':
    optimize(f, optimizer=SAESOptimizer(), timeout=1)