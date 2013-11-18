from time import sleep

import orges.param as param

@param.int("a", interval=(0, 1))
def f(a):
    return a

