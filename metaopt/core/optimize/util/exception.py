# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

class OptimizerError(Exception):
    """Indicates general error in optimizer."""
    def __init__(self, error):
        message = str(error.__class__.__name__) + ": "\
            + str(error)

        super(OptimizerError, self).__init__(message)

class MissingRequirementsError(Exception):
     def __init__(self, module_name='Not specified'):
        message = 'Please install required dependencies to use ' \
            + 'this optimizer: %s' % module_name
        super(MissingRequirementsError, self).__init__(message)

class WrongArgumentTypeError(Exception):
    """Indicates wrong type of parameters."""
    def __init__(self, message=None):
        super(WrongArgumentTypeError, self).__init__(message)

class GlobalTimeoutError(Exception):
    """Indicates that the the global timeout has occurred."""
    def __init__(self, message=None):
        super(GlobalTimeoutError, self).__init__(message)


class NoParamSpecError(Exception):
    """Indicates that no ParamSpec object was provided."""
    def __init__(self, message=None):
        super(NoParamSpecError, self).__init__(message)
