from collections import OrderedDict
from numbers import Integral


class ParamSpec(object):
    """
    An object describing the parameters of an algorithm.

    A parameter is either a fixed value or a description consisting of a type
    and optionally an interval with an associated step size.

    Parameters are specified like this::

        # A float parameter named "a" with values between 0 and 1
        param_spec.float("a", interval=(0, 1))

        # The values of "a" should only be multiple of 0.1
        param_spec.float("a", interval=(0, 1), step=0.1)

    The order the parameters are specified matters since they are used to invoke
    the actual algorithm. That is, given a function ``f(a, b)`` the parameter
    "a" should be specified before the parameter "b".

    """
    def __init__(self, via_decorator=False):
        self._params = []
        self.via_decorator = via_decorator

    @property
    def params(self):
        """
        The specified parameters as ordered dictionary

        Individual parameters can be accessed by using their name as key. To get
        all parameters as list use the ``values`` method.

        """
        ordered_params = OrderedDict()

        if self.via_decorator:
            for param in reversed(self._params):
                ordered_params[param.name] = param
        else:
            for param in self._params:
                ordered_params[param.name] = param

        return ordered_params

    def add_param(self, param):
        """Add a param to this param_spec object manually"""
        if param.name in self.params:
            raise DuplicateParamError(param)
        self._params.append(param)

    def float(self, name, interval, display_name=None, step=None):
        """Add a float param to this param_spec object"""
        param = Param(name, "float", interval,
            step=step, display_name=display_name)

        self.add_param(param)

    def int(self, name, interval, display_name=None, step=1):
        """Add an int param to this param_spec object"""
        param = IntParam(name, "int", interval,
            step=step, display_name=display_name)

        self.add_param(param)

    def bool(self, name, display_name=None):
        """Add a bool param to this param_spec object"""
        param = BoolParam(name, "bool", (True, False), display_name=display_name)
        self.add_param(param)


class Param(object):
    """A specified parameter consisting of a type, an interval and a step."""

    def __init__(self, name, type, interval, step=None, display_name=None):
        self._name = name
        self._type = type

        self._interval = interval
        self.check_interval()

        self._step = step
        self._display_name = display_name or name

    def check_interval(self):
        if self.lower_bound > self.upper_bound:
            raise InvalidIntervalError(self, self.interval)

    @property
    def name(self):
        """The name of the parameter """
        return self._name

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        self._display_name = display_name

    @property
    def type(self):
        """
        The type of the parameter.

        It can be one of the following values: float.

        """
        return self._type

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
        Param.__init__(self, *vargs, **kwargs)
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
        Param.__init__(self, *vargs, **kwargs)

    def check_interval(self):
        pass

class DuplicateParamError(Exception):
    """The error that occurs when two parameters with the same name are
         specified."""

    def __init__(self, param):
        Exception.__init__(self, "Duplicate parameter: %s" % (param.name,))
        self.param = param


class NonIntIntervalError(Exception):
    """The error that occurs when a non-intergral bound is specified"""

    def __init__(self, param, interval, index):
        Exception.__init__(
            self,
            "Interval [%s, %s] contains non-interger for parameter: %s"
            % (interval[0], interval[1], param.name)
        )

        self.param = param


class NonIntStepError(Exception):
    """The error that occurs when a non-integral is specified"""

    def __init__(self, param, step):
        Exception.__init__(
            self,
            "Step size (%s) is not an integer for parameter: %s"
            % (step, param.name)
        )
        self.param = param


class InvalidIntervalError(Exception):
    """The error that occurs when an invalid interval is specified"""

    def __init__(self, param, interval):
        Exception.__init__(
            self,
            "Lower bound (%s) is larger than upper bound (%s) for parameter: %s"
            % (interval[0], interval[1], param.name)
        )
        self.param = param