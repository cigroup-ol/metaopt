# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


class GlobalTimeoutError(Exception):
    """Indicates that the the global timeout has occurred."""
    def __init__(self, message=None):
        super(GlobalTimeoutError, self).__init__(message)


class NoParamSpecError(Exception):
    """Indicates that no ParamSpec object was provided."""
    def __init__(self, message=None):
        super(NoParamSpecError, self).__init__(message)
