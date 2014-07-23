# -*- coding: utf-8 -*-
"""
Using extra arguments
=====================

"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import maximize


@maximize("a*b")
@param.float("a", interval=[0, 1])
def f(a, b):
    return a + b


def main():
    from metaopt.core.optimize.optimize import optimize
    from metaopt.plugin.print.status import StatusPrintPlugin

    plugins = [
        StatusPrintPlugin(),
    ]

    for i in range(1, 10):
        optimum = optimize(f, timeout=1, extra_kwargs={"b": i}, plugins=plugins)
        print(optimum, "for i=%d" % i)

if __name__ == '__main__':
    main()
