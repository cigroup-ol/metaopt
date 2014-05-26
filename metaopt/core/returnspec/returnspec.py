# -*- coding: utf-8 -*-
"""
Classes to describe and work with the return values of objective functions
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.returnspec.util. \
    exception import MultiObjectivesNotSupportedError


DEFAULT_RETURN_VALUE_NAME = "Fitness"


class ReturnSpec(object):
    """
    This class describes the return values of an objective function

    Currently only single objective functions are supported.

    """
    def __init__(self, f=None, via_decorator=False):
        del via_decorator  # For future usage

        self.return_values = []

        if f:
            self.create_default_return_values(f)

    def create_default_return_values(self, f):
        del f  # TODO
        self.minimize(DEFAULT_RETURN_VALUE_NAME)

    def minimize(self, name):
        """Tells the optimizer to *minimize* the objective function"""
        return_value = self.create_return_value(name)
        return_value["minimize"] = True
        self.return_values.append(return_value)

    def maximize(self, name):
        """Tells the optimizer to *maximize* the objective function"""
        return_value = self.create_return_value(name)
        return_value["minimize"] = False
        self.return_values.append(return_value)

    def create_return_value(self, name):
        if not self.return_values:
            return {"name": name}
        else:
            raise MultiObjectivesNotSupportedError()
