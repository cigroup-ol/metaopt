class UnboundedArgIterError(Exception):
    """The error that occurs when an iter for an unbounded interval is used"""
    def __init__(self, param):
        message = "The interval %s is unbounded for parameter: %s" \
                  % (param.interval, param.name)
        super(UnboundedArgIterError, self).__init__(message)


class NoStepArgIterError(Exception):
    """The error that occurs when an iter with no given step size is used"""
    def __init__(self, param):
        message = "No step size specified for parameter: %s" % (param.name,)
        super(NoStepArgIterError, self).__init__(message)
