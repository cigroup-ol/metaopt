# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from numbers import Integral

# First Party
from metaopt.core.paramspec.util.exception import InvalidIntervalError, \
    NonIntIntervalError, NonIntStepError


class Param(object):
    """A specified parameter consisting of a type, an interval and a step."""

    def __init__(self, name, data_type, interval, step=None, title=None):
        self._name = name
        self._data_type = data_type

        self._interval = interval
        self.check_interval()

        self._step = step
        self._title = title or name

    def check_interval(self):
        if self.lower_bound > self.upper_bound:
            raise InvalidIntervalError(self, self.interval)

    @property
    def name(self):
        """The name of the parameter """
        return self._name

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def type(self):
        """
        The type of the parameter.

        It can be one of the following values: float.

        """
        return self._data_type

    @property
    def interval(self):
        """
        The interval specifying the allowed values of the parameter

        The interval is either a pair (from, to) that represents the closed
        interval [from, to].

        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        self._interval = interval

    @property
    def step(self):
        """
        The step size of the parameter.

        The step size represents the smallest meaningful change in the value of
        the parameter. A smaller change than the step size is expected to have
        no significant effect on the outcome of the algorithm or might not be
        even valid.

        """
        return self._step

    @step.setter
    def step(self, step):
        self._step = step

    @property
    def lower_bound(self):
        return self.interval[0]

    @property
    def upper_bound(self):
        return self.interval[1]


class IntParam(Param):
    def __init__(self, *vargs, **kwargs):
        super(IntParam, self).__init__(*vargs, **kwargs)

        self.check_step()

    def check_step(self):
        if not isinstance(self.step, Integral):
            raise NonIntStepError(self, self.step)

    def check_interval(self):
        if not isinstance(self.lower_bound, Integral):
            raise NonIntIntervalError(self, self.interval, 0)

        if not isinstance(self.upper_bound, Integral):
            raise NonIntIntervalError(self.param, self.interval, 1)

        Param.check_interval(self)


class BoolParam(Param):
    def __init__(self, *vargs, **kwargs):
        super(BoolParam, self).__init__(*vargs, **kwargs)

    def check_interval(self):
        pass
