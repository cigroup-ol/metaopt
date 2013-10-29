"""
Abstract invoker defining the API of invoker implementations.
"""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

import abc  # Abstract Base Class


class BaseInvoker(object):
    """Abstract invoker managing calls to ."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, resources, caller):
        pass

    @abc.abstractmethod
    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amout of resources of self."""
        pass

    @abc.abstractmethod
    def invoke(self, f, fargs, **kwargs):
        """Calls back to self.caller.on_result() for call(f, fargs)."""
        pass

    @abc.abstractmethod
    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        pass


class BaseCaller(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def on_result(self, return_value, fargs, **kwargs):
        pass

    @abc.abstractmethod
    def on_error(self, fargs, **kwargs):
        pass
