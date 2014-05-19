# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


import sys
if sys.version_info[0] == 2:
    # python 3 has an iterative zip built in
    from itertools import izip as zip


class ArgsModifier(object):
    '''
    Modifies args in useful ways.

    This module provides ways to modify given args. Specifically, args can be
    combined to each other and randomized with a certain strength.
    '''

    @staticmethod
    def combine(args1, args2):
        """Returns the combination of the elements of the two given args."""
        return [arg1.combine(arg2) for arg1, arg2 in zip(args1, args2)]

    @staticmethod
    def randomize(args, strengths):
        """Randomizes all of the given args with the given strength."""
        return [arg.randomize(strength) for arg, strength in
                zip(args, strengths)]
