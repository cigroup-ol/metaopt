"""
Interface definition and implementation of objects that can be stopped.
"""
from __future__ import division, print_function, with_statement

from abc import ABCMeta, abstractmethod, abstractproperty


class BaseStoppable(object):
    """Abstract object that can be stopped."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def stop(self):
        """
        Stops this object.

        Implementations of this method are expected to have the following
        behavior:

        Note that self should be stopped and return immediately. Do not accept
        to create new children and stop all running children.
        """
        pass

    @abstractproperty
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
    """
    Decorator that raises an StoppedException if self is stopped.

    Note that it needs to placed before an eventual stopping_method decorator.
    """
    def wrapped_method(self, *args, **kwargs):
        """The given method wrapped appended with test if self is stopped."""
        if self.stopped:
            raise StoppedException()
        return method(self, *args, **kwargs)
    return wrapped_method


def stopping_method(method):
    """
    Decorator that notes that is stopped.

    Note that it needs to placed after an eventual stoppable_method decorator.
    """
    def wrapped_method(self, *args, **kwargs):
        """The given method wrapped appended with test if self is stopped."""
        self._stopped = True  # Yes, access to the private attribute here
        return method(self, *args, **kwargs)
    return wrapped_method


class Stoppable(BaseStoppable):
    """An object that can be stopped."""

    def __init__(self):
        self._stopped = False

    @stoppable_method
    @stopping_method
    def stop(self):
        """"Stops this object."""
        pass  # implementations may overwrite this method or check for .stopped

    @property
    def stopped(self):
        """Indicates whether this object is stopped."""
        return self._stopped
