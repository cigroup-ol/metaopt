class StoppedError(Exception):
    """
    Indicates a call to an object that should *not* have been stopped before.
    """
    def __init__(self, message=None):
        super(StoppedError, self).__init__(message)


class NotStoppedError(Exception):
    """Indicates a call to an object that should have been stopped before."""
    def __init__(self, message=None):
        super(NotStoppedError, self).__init__(message)
