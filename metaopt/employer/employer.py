"""
Minimal employer implementation.
"""
from __future__ import division, print_function, with_statement

from metaopt.employer.base import BaseEmployer


class Employer(BaseEmployer):
    """
    Minimal employer implementation.
    """

    def __init__(self, resources=None):
        super(Employer, self).__init__()

        del resources

        self._worker_count = 0

    def employ(self):
        self._worker_count += 1

    def lay_off(self, call_id, reason=None):
        del call_id
        del reason

        self._worker_count -= 1

    def abandon(self, reason=None):
        del reason

        self._worker_count = 0

    @property
    def worker_count(self):
        return self._worker_count
