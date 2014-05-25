# -*- coding: utf-8 -*-
"""
Minimal invoker implementation.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.concurrent.invoker.base import BaseInvoker
from metaopt.core.call.call import call
from metaopt.core.returnspec.returnspec import ReturnSpec
from metaopt.core.stoppable.stoppable import stoppable


class Invoker(BaseInvoker):
    """
    Minimal invoker implementation.
    """

    def __init__(self):
        super(Invoker, self).__init__()

        self._f = None
        self._caller = None
        self._param_spec = None
        self._return_spec = None

    @property
    def f(self):
        """Property getter for the function attribute."""
        return self._f

    @f.setter
    def f(self, function):
        """Property setter for the function attribute."""
        self._f = function
        self._param_spec = function.param_spec
        self._return_spec = ReturnSpec(function)

    @property
    def param_spec(self):
        """Property getter for the parameter specification attribute."""
        return self._param_spec

    @param_spec.setter
    def param_spec(self, param_spec):
        """Property setter for the parameter specification attribute."""
        self._param_spec = param_spec

    @property
    def return_spec(self):
        """Property getter for the return specification attribute."""
        return self._return_spec

    @return_spec.setter
    def return_spec(self, return_spec):
        """Property setter for the return specification attribute."""
        self._return_spec = return_spec

    @stoppable
    def invoke(self, caller, fargs, **kwargs):
        self._caller = caller
        del caller
        call(self.f, fargs, **kwargs)

    def wait(self):
        return
