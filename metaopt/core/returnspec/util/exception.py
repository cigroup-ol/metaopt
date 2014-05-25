# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement


class MultiObjectivesNotSupportedError(Exception):
    def __init__(self, message=None):
        super(MultiObjectivesNotSupportedError, self).__init__(self, message)
