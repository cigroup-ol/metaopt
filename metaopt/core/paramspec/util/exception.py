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

        try:
            lower = interval[0]
        except IndexError:
            lower = None

        try:
            upper = interval[1]
        except IndexError:
            upper = None

        super(NonIntIntervalError, self).__init__(
            "Interval [%s, %s] contains non-integers for parameter: %s"
            % (lower, upper, param.name)
        )


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

class TitleForMultiParameterError(Exception):
    """The error that occurs when a title is specified for a multi parameter"""

    def __init__(self):
        super(TitleForMultiParameterError, self).__init__(
            "Specifying a title for a multi parameter is not currently "
            "supported"
        )

class MultiMultiParameterError(Exception):
    """The error that occurs when using a multi multi parameter"""

    def __init__(self):
        super(MultiMultiParameterError, self).__init__(
            "Multi multi parameters are not supported"
        )
