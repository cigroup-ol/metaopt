"""
Tests for the worker process provider.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from multiprocessing import Manager

# Third Party
import nose
from nose.tools.nontrivial import raises

# First Party
from metaopt.employer.process import ProcessWorkerEmployer
from metaopt.invoker.util.status_db import StatusDB


class TestWorkerProcessProvider(object):
    """
    Tests for the worker process provider.
    """

    def __init__(self):
        self._queue_outcome = None
        self._queue_start = None
        self._queue_task = None
        self.provider = None

    def setup(self):
        """Nose will run this method before every test method."""
        manager = Manager()
        self._queue_task = manager.Queue()  # ignore error, this works
        self._queue_start = manager.Queue()  # ignore error, this works
        self._queue_outcome = manager.Queue()  # ignore error, this works

        self._status_db = StatusDB(queue_task=self._queue_task,
                                   queue_start=self._queue_start,
                                   queue_outcome=self._queue_outcome)
        self.provider = ProcessWorkerEmployer(queue_tasks=self._queue_task,
                                              queue_outcome=self._queue_outcome,
                                              queue_start=self._queue_start,
                                              status_db=self._status_db)

    def teardown(self):
        """Nose will run this method after every test method."""
        self.provider.abandon()

    def test_worker_process_provider_employ_once(self):
        """
        A worker process provider can employ a worker process.
        """
        self.provider.employ()

    def test_worker_process_provider_employ_repeated(self):
        """
        A worker process provider can employ multiple worker processes.
        """
        number_of_workers = 1
        for _ in range(1, 10):
            self.provider.employ(number_of_workers=number_of_workers)
            assert self.provider.worker_count == number_of_workers
            self.provider.abandon()

    @raises(IndexError)
    def test_worker_process_provider_employ_too_many(self):
        """
        A worker process provider can employ a limited number of workers.
        """
        # Try to employ a lot of workers.
        for number_of_workers in [_ ** _ for _ in range(0, 100)]:
            self.provider.employ(number_of_workers=number_of_workers)

    def test_worker_process_provider_employ_layoff_once(self):
        """
        A worker process provider can employ and layoff a worker process.
        """
        self.provider.employ()
        self.provider.abandon()

    def test_worker_process_provider_employ_layoff_twice(self):
        """
        A worker process provider can employ a worker process repeatedly.
        """
        # once
        self.provider.employ()
        self.provider.abandon()

        # and once more
        self.provider.employ()
        self.provider.abandon()

    def test_worker_process_provider_initializes_count(self):
        """A worker process provider begins to count at 0."""
        assert self.provider.worker_count == 0

    def test_worker_process_provider_counts_up(self):
        """A worker process provider counts in increments of 1."""
        self.provider.employ(1)
        assert self.provider.worker_count == 1

    def test_worker_process_provider_counts_up_down(self):
        """A worker process provider counts up and down."""
        self.provider.employ(1)
        assert self.provider.worker_count == 1
        self.provider.abandon()
        assert self.provider.worker_count == 0

    def test_worker_process_provider_counts_up_down_twice(self):
        """A worker process provider counts up and down repeatedly."""
        # once
        self.provider.employ(1)
        assert self.provider.worker_count == 1
        self.provider.abandon()
        assert self.provider.worker_count == 0

        # and once more
        self.provider.employ(1)
        assert self.provider.worker_count == 1
        self.provider.abandon()
        assert self.provider.worker_count == 0

    def test_worker_process_provider_is_borg(self):
        """There can only be one instance of a worker process provider."""
        my_provider = ProcessWorkerEmployer(queue_tasks=self._queue_task,
                                            queue_outcome=self._queue_outcome,
                                            queue_start=self._queue_start,
                                            status_db=self._status_db)

        number_of_workers = 1

        # left
        self.provider.employ(number_of_workers=number_of_workers)
        assert self.provider.worker_count == number_of_workers
        assert self.provider.worker_count == my_provider.worker_count

        # right
        my_provider.employ(number_of_workers=number_of_workers)
        assert self.provider.worker_count == number_of_workers * 2
        assert self.provider.worker_count == my_provider.worker_count

    def test_worker_process_provider_employ_and_stop_multiple_workers(self):
        """Workers can be employed and laid off repeatedly."""
        worker_count = 2  # any number more than one proves the point

        # once
        self.provider.employ(number_of_workers=worker_count)
        self.provider.abandon()

        # and once more
        self.provider.employ(number_of_workers=worker_count)
        self.provider.abandon()

if __name__ == '__main__':
    nose.runmodule()
