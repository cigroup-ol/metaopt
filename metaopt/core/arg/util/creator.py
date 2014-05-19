# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import itertools

# First Party
from metaopt.core.arg.util.create_arg import create_arg


class ArgsCreator(object):
    """
    Creates args in useful ways.

    This module is responsible for creating actual args from params that are
    defined in a ParamSpec. Args can be created in a random or systematic way.
    """
    def __init__(self, param_spec):
        self.param_spec = param_spec

    def args(self):
        """Returns an args derived from the params given on instantiation."""
        return [create_arg(param) for param in self.param_spec.params.values()]

    def random(self):
        """Returns a randomized version of self.args()."""
        return [arg.random() for arg in self.args()]

    def product(self):
        """Iterator that iterates over all args combinations"""
        return itertools.product(*self.args())
