# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import random

# First Party
from metaopt.core.arg.arg import Arg


class BoolArg(Arg):
    def __init__(self, param, value=None):
        super(BoolArg, self).__init__(param=param, value=value)

    def random(self):
        return BoolArg(self.param, value=random.choice([True, False]))

    def randomize(self, strength):
        del strength  # TODO
        return self.random()

    def combine(self, other_arg):
        value = self.value or other_arg.value
        return BoolArg(self.param, value=value)

    def __iter__(self):
        if self.value:
            yield BoolArg(self.param, True)
        yield BoolArg(self.param, False)
