"""
Abstract invoker defining the API of invoker implementations.
"""

from __future__ import division, print_function, with_statement

import abc


class BaseInvoker(object):
    """Abstract invoker managing calls to call(f, fargs)."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, caller):
        pass

    @abc.abstractmethod
    def invoke(self, f, fargs, **kwargs):
        """
        Implementations of this method should have the following behavior:

        Invokes call(f, fargs) with the given function and the given arguments.
        Calls back to self.caller.on_result() for successful invokes.
        Calls back to self.caller.on_error() for unsuccessful invokes.
        Can be called asynchronously, but will block if the call can not be
        executed immediately, especially when using multiple processes/threads.
        """
        pass

    @abc.abstractmethod
    def wait(self):
        """
        Implementations of this method should have the following behavior:

        Blocks till all invoke, on_error or on_result calls are done.
        """
        pass

    @abc.abstractmethod
    def abort(self):
        """
        Implementations of this method should have the following behavior:

        Cancels all running and future tasks.
        """
        pass
