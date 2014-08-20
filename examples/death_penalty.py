# -*- coding: utf-8 -*-
"""
Example of optimization with death penalty.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import minimize


@minimize("a-b")
@param.float("a", interval=[0, 1])
@param.float("b", interval=[0, 1])
def f(a, b):
    assert a > b, "a should be greater than b"
    return a - b

def main():
    from metaopt.core.optimize.optimize import optimize
    from metaopt.plugin.print.status import StatusPrintPlugin

    plugins = [
        StatusPrintPlugin(),
    ]

    print(optimize(f, timeout=100, plugins=plugins))


if __name__ == '__main__':
    main()
