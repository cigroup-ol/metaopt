# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import random
from random import randint

# First Party
from metaopt.core.arg.arg import Arg


class IntArg(Arg):
    """
    TODO
    """
    def __init__(self, param, value=None):
        super(IntArg, self).__init__(param=param, value=value)

    def random(self):
        value = randint(self.param.lower_bound, self.param.upper_bound)
        return IntArg(self.param, value=value)

    def randomize(self, strength):
        value = int(self.value + random.gauss(0, 1) * strength)

        if value < self.param.lower_bound:
            value = self.param.lower_bound
        elif value > self.param.upper_bound:
            value = self.param.upper_bound

        return IntArg(self.param, value=value)

    def combine(self, other_arg):
        value = (self.value + other_arg.value) / 2
        return IntArg(self.param, int(value))
