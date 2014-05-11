# -*- coding: utf-8 -*-
"""
Minimal caller implementation.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.optimizer.base import BaseCaller


class Caller(BaseCaller):
    """
    Minimal caller implementation.
    """

    def __init__(self):
        super(Caller, self).__init__()

    def on_result(self, value, fargs, **kwargs):
        raise NotImplementedError()

    def on_error(self, value, fargs, **kwargs):
        raise NotImplementedError()
