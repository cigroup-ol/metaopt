# -*- coding: utf-8 -*-
"""
Interface definition and implementation of objects that can be stopped.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.stoppable.base import BaseStoppable
from metaopt.core.stoppable.util.decorator import stoppable, stopping


class Stoppable(BaseStoppable):
    """An object that can be stopped."""

    def __init__(self):
        super(Stoppable, self).__init__()

        self._stopped = False

    @stoppable
    @stopping
    def stop(self, reason=None):
        """"Stops this object."""
        del reason  # implementations may overwrite and use the optional reason
        self._stopped = True

    @property
    def stopped(self):
        """Indicates whether this object is stopped."""
        return self._stopped
