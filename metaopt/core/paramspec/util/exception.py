class DuplicateParamError(Exception):
    """The error that occurs when two parameters with the same name are
         specified."""

    def __init__(self, param):
        super(DuplicateParamError, self).__init__("Duplicate parameter: %s"
                                                  % (param.name,))
        self.param = param


class NonIntIntervalError(Exception):
    """The error that occurs when a non-intergral bound is specified"""

    def __init__(self, param, interval, index):
        del index  # TODO

        message = "Interval [%s, %s] contains non-interger for parameter: %s" \
                  % (interval[0], interval[1], param.name)
        super(NonIntIntervalError, self).__init__(message)


class NonIntStepError(Exception):
    """The error that occurs when a non-integral is specified"""

    def __init__(self, param, step):
        message = "Step size (%s) is not an integer for parameter: %s" \
                  % (step, param.name)
        super(NonIntStepError, self).__init__(message)


class InvalidIntervalError(Exception):
    """The error that occurs when an invalid interval is specified"""

    def __init__(self, param, interval):
        message = ("Lower bound (%s) larger than upper bound (%s) " + \
                   "for parameter: %s") \
                  % (interval[0], interval[1], param.name)

        super(InvalidIntervalError, self).__init__(message)
        self.param = param
