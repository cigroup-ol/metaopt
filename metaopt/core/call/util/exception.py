class CallNotPossibleError(Exception):
    def __init__(self, msg):
        super(CallNotPossibleError, self).__init__(msg)
