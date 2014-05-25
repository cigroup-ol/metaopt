# -*- coding: utf-8 -*-
"""
Interface definition and implementation of objects that can be stopped.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from abc import ABCMeta, abstractmethod


class BaseStoppable(object):
    """Abstract object that can be stopped."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        super(BaseStoppable, self).__init__()

    @abstractmethod
    def stop(self, reason=None):
        """
        Stops this object.

        Implementations of this method are expected to have the following
        behavior:

        Note that self should be stopped and return immediately. Do not accept
        to create new children and stop all running children.
        """
        pass

    @property
    @abstractmethod
    def stopped(self):
        """
        Indicates whether this object is stopped.

        Implementations should return if stop() was called before.
        """
        pass
