# -*- coding: utf-8 -*-
"""
Minimal employer implementation.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.concurrent.employer.base import BaseEmployer


class Employer(BaseEmployer):
    """
    Minimal employer implementation.
    """

    def __init__(self, resources=None):
        super(Employer, self).__init__()

        del resources

        self._worker_count = 0

    def employ(self, number_of_workers=1):
        self._worker_count += number_of_workers

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
