# -*- coding: utf-8 -*-
"""
SVM (SAES, global timeout)
================================
"""
from __future__ import division, print_function, with_statement

from time import sleep

from sklearn import cross_validation, datasets, svm

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

    optimizer = GridSearchOptimizer()

    plugins = [
        PrintPlugin(),
    ]

    print(optimize(f, timeout=3, optimizer=optimizer, plugins=plugins))

if __name__ == '__main__':
    main()
