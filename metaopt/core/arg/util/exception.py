class UnboundedArgIterError(Exception):
    """The error that occurs when an iter for an unbounded interval is used"""
    def __init__(self, param):
        super(UnboundedArgIterError, self).__init__(
            self,
            "The interval %s is unbounded for parameter: %s"
            % (param.interval, param.name)
        )


class NoStepArgIterError(Exception):
    """The error that occurs when an iter with no given step size is used"""
    def __init__(self, param):
        super(NoStepArgIterError, self).__init__(
            self,
            "No step size specified for parameter: %s"
            % (param.name,)
        )
