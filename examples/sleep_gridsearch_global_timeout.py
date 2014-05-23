# -*- coding: utf-8 -*-
"""
SVM (SAES, global timeout)
================================
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from time import sleep

# First Party
from metaopt.core.param.util import param
from metaopt.core.returns.util.decorator import maximize


@maximize("Score")
@param.int("a", interval=[1, 9])
def f(a):
    sleep(2)
    return 0


def main():
    from metaopt.core.main import optimize
    from metaopt.optimizer.gridsearch import GridSearchOptimizer
    from metaopt.plugin.print.status import StatusPrintPlugin

    timeout = 3
    optimizer = GridSearchOptimizer()
    plugins = [StatusPrintPlugin()]

    optimum = optimize(f=f, timeout=timeout, optimizer=optimizer,
                       plugins=plugins)

    print("The optimal parameters are %s." % str(optimum))

if __name__ == '__main__':
    main()
