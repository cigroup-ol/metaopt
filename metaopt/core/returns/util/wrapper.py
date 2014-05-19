class ReturnValuesWrapper(object):
    """
    Wraps a return specification and a set of corresponding return values.

    Enables comparison between value sets.
    """
    def __init__(self, return_spec, values):
        self.return_spec = return_spec
        self.values = values

    # TODO: Use something like functools.total_ordering
    def __lt__(self, other):
        if self.minimization:
            return self.values < other.values
        else:
            return self.values > other.values

    def __eq__(self, other):
        return not self < other and not other < self

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return repr(self.values)

    @property
    def raw_values(self):
        """The unwrapped values"""
        return self.values

    @property
    def minimization(self):
        if not self.return_spec:
            return True
        else:
            return self.return_spec.return_values[0]["minimize"]
