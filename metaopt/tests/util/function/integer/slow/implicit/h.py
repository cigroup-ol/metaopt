from __future__ import division, print_function, with_statement

from time import sleep


def f():
    """Function that hangs indefinitely."""
    while True:
        sleep(1)
