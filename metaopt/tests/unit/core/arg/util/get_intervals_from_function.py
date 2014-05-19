# -*- coding: utf-8 -*-
"""
Utilities for writing unit tests for the core.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


def get_intervals_from_function(function):
    """Returns a dictionary of parameter titles and ranges."""
    intervals = dict()
    for key in function.param_spec.params.keys():
        intervals[key] = function.param_spec.params[key].interval
    return intervals
