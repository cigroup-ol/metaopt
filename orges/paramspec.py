from collections import OrderedDict
from inspect import getargspec
from numbers import Integral


class ParamSpec(object):
    """
    An object describing the parameters of an algorithm.

    A parameter is either a fixed value or a description consisting of a type
    and optionally an interval with an associated step size.

    Parameters are specified using chained method invocations like this::

        # A float parameter named "a" with values between 0 and 1
        param_spec.float("a").interval((0, 1))

        # The values of "a" should only be multiple of 0.1
        param_spec.float("a").interval((0, 1)).step(0.1)

        # A float parameter named "b" with all values being allowed
        param_spec.float("b")

        # The values of "b" should only be changed in steps of size 0.2
        param_spec.float("b").all().step(0.2)

        # A float parameter named "c" with no upper bound
        param_spec.float("c").interval(0, None)

    The order the parameters are specified matters since they are used to invoke
    the actual algorithm. That is, given a function ``f(a, b)`` the parameter
    "a" should be specified before the parameter "b".

    """
    def __init__(self, f=None):
        self._params = OrderedDict()

    @property
    def params(self):
        """
        The specified parameters as ordered dictionary

        Individual parameters can be accessed by using their name as key. To get
        all parameters as list use the ``values`` method.

        """
        return self._params

    def add_param(self, param):
        if param.name in self._params:
            raise DuplicateParamError(param)
        self._params[param.name] = param

    def infer_params(self, f):
        args, vargs, kwargs, _ = getargspec(f)

        if vargs is not None:
            raise InferNotPossibleError(
                "Cannot infer parameters for variable arguments.")

        if kwargs is not None:
            raise InferNotPossibleError(
                "Cannot infer parameters for keyword arguments.")

        for arg in args:
            self.add_param(Param(arg, "float"))

    def float(self, name, interval=(None,None), display_name=None, step=None):

        param = Param(name, "float", interval,
            step=step, display_name=display_name)

        self.add_param(param)

    def int(self, name, interval=(None, None), display_name=None, step=1):
        param = IntParam(name, "int", interval,
            step=step, display_name=display_name)

        self.add_param(param)

    def bool(self, name, display_name=None):
        param = BoolParam(name, "bool", (True, False), display_name=display_name)
        self.add_param(param)


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


class InferNotPossibleError(Exception):
    """The error that occurs when parameters cannot be infered"""
    def __init__(self, msg):
        Exception.__init__(self, msg)


class Param(object):
    """A specified parameter consisting of a type, an interval and a step."""

    def __init__(self, name, type, interval=None, step=None, display_name=None):
        self._name = name
        self._type = type

        self._interval = interval
        self.check_interval()

        self._step = step
        self._display_name = display_name

        if display_name is None:
            self._display_name = name

    def check_interval(self):
        if self.interval[0] is not None and self.interval[1] is not None\
                and self.interval[0] > self.interval[1]:
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
        interval [from, to] or None specifying that all values are valid. If
        ``from`` or ``to`` is None there is no lower or upper bound.

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

class IntParam(Param):
    def __init__(self, *vargs, **kwargs):
        Param.__init__(self, *vargs, **kwargs)
        self.check_step()

    def check_step(self):
        if not isinstance(self.step, Integral):
            raise NonIntStepError(self, self.step)

    def check_interval(self):
        if self.interval[0] is not None\
                and not isinstance(self.interval[0], Integral):
            raise NonIntIntervalError(self, self.interval, 0)

        if self.interval[1] is not None\
                and not isinstance(self.interval[1], Integral):
            raise NonIntIntervalError(self.param, self.interval, 1)

        if self.interval[0] is not None and self.interval[1] is not None\
                and self.interval[0] > self.interval[1]:
            raise InvalidIntervalError(self, self.interval)

        Param.check_interval(self)

class BoolParam(Param):
    def __init__(self, *vargs, **kwargs):
        Param.__init__(self, *vargs, **kwargs)

    def check_interval(self):
        pass


if __name__ == '__main__':
    pass
