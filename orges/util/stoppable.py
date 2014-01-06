"""
Interface definition and implementation of objects that can be stopped.
"""
from __future__ import division, print_function, with_statement

import abc


class BaseStoppable(object):
    """Abstract object that can be stopped."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stop(self):
        """
        Stops this object.

        Implementations of this method are expected to have the following
        behavior:

        Note that self should be stopped and return immediately. Do not accept
        to create new children and stop all running children.
        """
        pass

    @abc.abstractproperty
    def stopped(self):
        """
        Indicates whether this object is stopped.

        Implementations should return if stop() was called before.
        """
        pass


class StoppedException(Exception):
    """Indicates that a call was made to a stopped object."""
    pass


def stoppable_method(method):
    """Decorator that raises an StoppedException if self is stopped."""

    def wrapped_method(self, *args, **kwargs):
        """The given method wrapped appended with test if self is stopped."""
        if self.stopped:
            raise StoppedException()
        return method(self, *args, **kwargs)
    return wrapped_method


class Stoppable(BaseStoppable):
    """An object that can be stopped."""

    def __init__(self):
        self._stopped = False

    @stoppable_method
    def stop(self):
        """"Stops this object."""
        self._stopped = True

    @property
    def stopped(self):
        """Indicates whether this object is stopped."""
        return self._stopped
