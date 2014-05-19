# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import random

# First Party
from metaopt.core.arg.util.exception import NoStepArgIterError, \
    UnboundedArgIterError


class Arg(object):
    """

    An Arg is a container for a value that is associated with a parameter.

    An Arg also provides various ways to create new Arg objects (that are
    possibly based on a previous value). To get the actual value use
    :attr:`value`.

    An arg is something that contains a value that respects the constraints
    (e.g. interval with step size) defined by the corresponding param.

    For instance, given an int param ``param_spec.int("a", interval=(1,10))``
    a corresponding arg could be ``a=1``.

    """

    def __init__(self, param, value=None):
        self.param = param
        self.value = value

        if self.value is None:
            self.value = self.param.interval[0]

    def random(self):
        value = random.uniform(self.param.lower_bound, self.param.upper_bound)

        if value < self.param.lower_bound:
            value = self.param.lower_bound
        elif value > self.param.upper_bound:
            value = self.param.upper_bound

        return Arg(self.param, value)

    def randomize(self, strength):
        value = self.value + random.gauss(0, 1) * strength

        if value < self.param.lower_bound:
            value = self.param.lower_bound
        elif value > self.param.upper_bound:
            value = self.param.upper_bound

        return Arg(self.param, value)

    def combine(self, other_arg):
        value = (self.value + other_arg.value) / 2
        return Arg(self.param, value)

    def __iter__(self):
        if None in self.param.interval:
            raise UnboundedArgIterError(self.param)

        if self.param.step is None:
            raise NoStepArgIterError(self.param)

        current = self

        while current.value < current.param.interval[1]:
            yield current
            current = Arg(current.param, current.value + current.param.step)

        yield Arg(self.param, self.param.interval[1])

    def __repr__(self):
        return "%s=%s" % (self.param.title, self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not self == other
