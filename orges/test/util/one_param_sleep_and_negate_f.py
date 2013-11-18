"""
TODO document me
"""

from time import sleep
from orges import param

@param.int("a", interval=(0, 1))
def f(a):
    sleep(2)
    return -a
