from __future__ import division, print_function, with_statement

import orges.param as param

@param.int("a", interval=(0, 1))
def f(a):
    return a

