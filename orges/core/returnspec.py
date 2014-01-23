"""
Classes to describe an work with the return ReturnValuesWrapper of objective functions
"""
from __future__ import division, print_function, with_statement

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
        self.maximize(DEFAULT_RETURN_VALUE_NAME)

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


class MultiObjectivesNotSupportedError(Exception):
    pass


class ReturnValuesWrapper(object):
    def __init__(self, return_spec, values):
        self.return_spec = return_spec
        self.values = values

    def __cmp__(self, other):
        real_cmp = cmp(self.values, other.values)
        reverse_cmp = -1 * real_cmp

        if self.is_minimization():
            return real_cmp
        else:
            return reverse_cmp

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return repr(self.values)

    def is_minimization(self):
        return self.return_spec.return_values[0]["minimize"]
