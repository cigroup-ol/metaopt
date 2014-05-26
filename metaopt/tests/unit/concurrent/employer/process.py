# -*- coding: utf-8 -*-
"""
Tests for the worker process _employer.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from multiprocessing import Manager

# Third Party
import nose
from mock import Mock
from nose.tools.nontrivial import raises

# First Party
from metaopt.concurrent.employer.process import ProcessWorkerEmployer


class TestProcessWorkerEmployer(object):
    """
    Tests for the worker process _employer.
    """

    def __init__(self):
        self._queue_outcome = None
        self._queue_start = None
        self._queue_task = None
        self._employer = None

    def setup(self):
        """Nose will run this method before every test method."""
        manager = Manager()
        self._queue_task = manager.Queue()  # ignore error, this works
        self._queue_start = manager.Queue()  # ignore error, this works
        self._queue_outcome = manager.Queue()  # ignore error, this works

        self._status_db = Mock()
        self._status_db.get_running_call = Mock(return_value=None)
        self._employer = ProcessWorkerEmployer(queue_tasks=self._queue_task,
                                              queue_outcome=self._queue_outcome,
                                              queue_start=self._queue_start,
                                              status_db=self._status_db)

    def teardown(self):
        """Nose will run this method after every test method."""
        self._employer.abandon()

    def test_employ_once(self):
        """
        A worker process _employer can employ a worker process.
        """
        self._employer.employ()

    def test_employ_repeated(self):
        """
        A worker process _employer can employ multiple worker processes.
        """
        number_of_workers = 1
        for _ in range(1, 10):
            self._employer.employ(number_of_workers=number_of_workers)
            assert self._employer.worker_count == number_of_workers
            self._employer.abandon()

    @raises(IndexError)
    def test_employ_too_many(self):
        """
        A worker process employer can employ a limited number of workers.
        """
        # Try to employ a lot of workers.
        for number_of_workers in [_ ** _ for _ in range(0, 100)]:
            self._employer.employ(number_of_workers=number_of_workers)

    def test_employ_and_layoff_once(self):
        """
        A worker process employer can employ and layoff a worker process.
        """
        self._employer.employ()
        self._employer.abandon()

    def test_employ_layoff_twice(self):
        """
        A worker process employer can employ a worker process repeatedly.
        """
        # once
        self._employer.employ()
        self._employer.abandon()

        # and once more
        self._employer.employ()
        self._employer.abandon()

    def test_initialize_count(self):
        """A worker process _employer begins to count at 0."""
        assert self._employer.worker_count == 0

    def test_count_up(self):
        """A worker process _employer counts in increments of 1."""
        self._employer.employ(1)
        assert self._employer.worker_count == 1

    def test_count_up_down(self):
        """A worker process _employer counts up and down."""

        self._employer.employ(1)
        assert self._employer.worker_count == 1
        self._employer.abandon()
        assert self._employer.worker_count == 0

    def test_count_up_down_twice(self):
        """A worker process employer counts up and down repeatedly."""
        # once
        self._employer.employ(1)
        assert self._employer.worker_count == 1
        self._employer.abandon()
        assert self._employer.worker_count == 0

        # and once more
        self._employer.employ(1)
        assert self._employer.worker_count == 1
        self._employer.abandon()
        assert self._employer.worker_count == 0

    def test_is_borg(self):
        """There can only be one instance of a worker process _employer."""
        my_provider = ProcessWorkerEmployer(queue_tasks=self._queue_task,
                                            queue_outcome=self._queue_outcome,
                                            queue_start=self._queue_start,
                                            status_db=self._status_db)

        number_of_workers = 1

        # left
        self._employer.employ(number_of_workers=number_of_workers)
        assert self._employer.worker_count == number_of_workers
        assert self._employer.worker_count == my_provider.worker_count

        # right
        my_provider.employ(number_of_workers=number_of_workers)
        assert self._employer.worker_count == number_of_workers * 2
        assert self._employer.worker_count == my_provider.worker_count

    def test_employ_and_stop_multiple_workers(self):
        """Workers can be employed and laid off repeatedly."""
        worker_count = 2  # any number more than one proves the point

        # once
        self._employer.employ(number_of_workers=worker_count)
        self._employer.abandon()

        # and once more
        self._employer.employ(number_of_workers=worker_count)
        self._employer.abandon()

if __name__ == '__main__':
    nose.runmodule()
