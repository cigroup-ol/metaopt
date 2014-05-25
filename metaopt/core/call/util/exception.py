# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


class CallNotPossibleError(Exception):
    def __init__(self, message=None):
        super(CallNotPossibleError, self).__init__(message)
