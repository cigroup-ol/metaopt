# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from time import sleep


def f():
    """Function that hangs indefinitely."""
    while True:
        sleep(1)
