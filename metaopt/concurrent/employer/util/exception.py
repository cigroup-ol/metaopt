# -*- coding: utf-8 -*-
"""
Exceptions for managing workers.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


class LayoffError(Exception):
    """Indicates that a worker got laid off."""

    def __init__(self, message=None):
        super(LayoffError, self).__init__(message)
