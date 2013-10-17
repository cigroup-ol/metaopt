"""Returns always the same arguments for the hang module c extension."""


class ArgsIterator:
    def __init__(self):
        self.current = 100

    def __iter__(self):
        return self

    def next(self):
        return self.current
