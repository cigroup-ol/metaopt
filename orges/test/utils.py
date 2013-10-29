from time import sleep

import orges.param as param

@param.int("a", interval=(0, 1))
def one_param_f(a):
    return a

@param.int("a", interval=(0, 1))
def one_param_sleep_and_negate_f(a):
    sleep(2)
    return -a
