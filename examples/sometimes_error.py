# -*- coding: utf-8 -*-
"""
TODO
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from random import randint

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import maximize


@maximize("a+b")
@param.float("a", interval=[0, 1])
@param.float("b", interval=[0, 1])
def f(a, b):
    if randint(1, 3) == 1:
        raise Exception("Some Error")
    return a + b

def main():
    from metaopt.core.optimize.optimize import optimize
    from metaopt.plugin.print.status import StatusPrintPlugin

    plugins = [
        StatusPrintPlugin(),
    ]

    print(optimize(f, timeout=1, plugins=plugins))


if __name__ == '__main__':
    main()
