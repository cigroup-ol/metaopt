# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util.exception import DuplicateParamError
from metaopt.core.paramspec.util.model import BoolParam, IntParam, Param


try:
    from collections import OrderedDict
except ImportError:
    # Python < 2.7
    from ordereddict import OrderedDict


class ParamSpec(object):
    """
    An object describing the parameters of an algorithm.

    A parameter is either a fixed value or a description consisting of a type
    and optionally an interval with an associated step size.

    Parameters are specified like this::

        # A float parameter named "a" with values between 0 and 1
        param_spec.float("a", interval=(0, 1))

        # The values of "a" should only be multiple of 0.1
        param_spec.float("a", interval=(0, 1), step=0.1)

    The order the parameters are specified matters since they are used to
    invoke the actual algorithm. That is, given a function ``f(a, b)`` the
    parameter "a" should be specified before the parameter "b".

    """
    def __init__(self, via_decorator=False):
        self._params = []
        self.via_decorator = via_decorator

    @property
    def params(self):
        """
        The specified parameters as ordered dictionary

        Individual parameters can be accessed by using their name as key. To
        get all parameters as list use the ``values`` method.

        """
        ordered_params = OrderedDict()

        if self.via_decorator:
            for param in reversed(self._params):
                ordered_params[param.name] = param
        else:
            for param in self._params:
                ordered_params[param.name] = param

        return ordered_params

    def add_param(self, param):
        """Add a param to this param_spec object manually"""
        if param.name in self.params:
            raise DuplicateParamError(param)
        self._params.append(param)

    def float(self, name, interval, title=None, step=None):
        """Add a float param to this param_spec object"""
        param = Param(name, "float", interval,
                      step=step, title=title)

        self.add_param(param)

    def int(self, name, interval, title=None, step=1):
        """Add an int param to this param_spec object"""
        param = IntParam(name, "int", interval,
                         step=step, title=title)

        self.add_param(param)

    def bool(self, name, title=None):
        """Add a bool param to this param_spec object"""
        param = BoolParam(name, "bool", (True, False), title=title)
        self.add_param(param)
