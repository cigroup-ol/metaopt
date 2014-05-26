# -*- coding: utf-8 -*-
"""
Matchers for Mock.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import itertools
import string

# First Party
from metaopt.core.returnspec.returnspec import ReturnSpec


class EqualityMatcher(object):
    """
    Checks if two elements have the same value.

    This is a workaround to the fact that Mock will check if the *same* object
    is returned, which is never the case for objects that were pickled, as is
    required for interprocess communication (IPC) done by the
    MultiProcessInvoker.
    """
    def __init__(self, one):
        self.one = one

    def __eq__(self, other):
        if isinstance(self.one, itertools.product):
            try:
                for x, y in zip(self.one, other):
                    if x != y:
                        return False
                return True
            except TypeError:
                return False

        if type(self.one) != type(other):
            raise TypeError("One (%s) and other (%s) are of different types."
                            % (type(self.one), type(other)))

        if type(self.one) == int and type(other) == int:
            return self.one == other
        if type(self.one) == string and type(other) == string:
            return self.one == other
        if type(self.one) == list and type(other) == list:
            for a, b in zip(self.one, other):
                if not a.value == b.value:
                    return False
            return True
        if type(self.one) == dict and type(other) == dict:
            for key, value in self.one:
                if not other[key] == value:
                    return False
            return True
        if type(self.one) == ReturnSpec and type(other) == ReturnSpec:
            return self.one.return_values == other.return_values
        if repr(self.one) == repr(other):
            return True
        raise NotImplementedError(type(self.one), type(other))
