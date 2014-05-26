# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.stoppable.util.exception import StoppedError


def stoppable(method):
    """
    Decorator that raises an StoppedError if self is stopped.

    Note that it needs to placed before an eventual stopping decorator.
    """
    def wrapped_method(self, *args, **kwargs):
        """The given method wrapped appended with test if self is stopped."""
        if self.stopped:
            raise StoppedError()
        return method(self, *args, **kwargs)
    return wrapped_method


def stopping(method):
    """
    Decorator that notes that is stopped.

    Note that it needs to placed after an eventual stoppable decorator.
    """
    def wrapped_method(self, *args, **kwargs):
        """The given method wrapped appended with test if self is stopped."""
        self._stopped = True  # Yes, access to the private attribute here
        return method(self, *args, **kwargs)
    return wrapped_method
