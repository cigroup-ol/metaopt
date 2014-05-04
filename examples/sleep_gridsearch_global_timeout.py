# -*- coding: utf-8 -*-
"""
SVM (SAES, global timeout)
================================
"""
from __future__ import division, print_function, with_statement

from time import sleep

from metaopt.core import param
from metaopt.core.returns import maximize


@maximize("Score")
@param.int("a", interval=[1, 9])
def f(a):
    sleep(2)
    return 0


def main():
    from metaopt.core.main import optimize
    from metaopt.optimizer.gridsearch import GridSearchOptimizer
    from metaopt.plugins.print import PrintPlugin

    timeout = 3
    optimizer = GridSearchOptimizer()
    plugins = [PrintPlugin()]

    optimum = optimize(f=f, timeout=timeout, optimizer=optimizer,
                       plugins=plugins)

    print("The optimal parameters are %s." % str(optimum))

if __name__ == '__main__':
    main()
