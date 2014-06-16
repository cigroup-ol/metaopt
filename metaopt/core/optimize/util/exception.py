# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

class OptimizerException(Exception):
    """Indicates general error in optimizer."""
    def __init__(self, message=None):
        super(OptimizerException, self).__init__(message)

class WrongArgumentTypeException(Exception):
    """Indicates wrong type of parameters."""
    def __init__(self, message=None):
        super(WrongArgumentTypeException, self).__init__(message)

class GlobalTimeoutError(Exception):
    """Indicates that the the global timeout has occurred."""
    def __init__(self, message=None):
        super(GlobalTimeoutError, self).__init__(message)


class NoParamSpecError(Exception):
    """Indicates that no ParamSpec object was provided."""
    def __init__(self, message=None):
        super(NoParamSpecError, self).__init__(message)
