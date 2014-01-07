"""
Utilities for writing unit tests for the core.
"""
from __future__ import division, print_function, with_statement


def get_intervals_from_function(function):
    """Returns a dictionary of parameter titles and ranges."""
    return {key: function.param_spec.params[key].interval
            for key in function.param_spec.params.keys()}
