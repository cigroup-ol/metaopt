"""
Tests for the worker process provider.
"""
from __future__ import division, print_function, with_statement

from multiprocessing import Manager

import nose
from nose.tools.nontrivial import raises

from metaopt.invoker.util.worker_provider import WorkerProcessProvider


class TestWorkerProcessProvider(object):
    """
    Tests for the worker process provider.
    """

    def __init__(self):
        self.queue_results = None
        self.queue_status = None
        self.queue_tasks = None
        self.provider = None

    def setup(self):
        """Nose will run this method before every test method."""
        manager = Manager()
        self.queue_tasks = manager.Queue()  # ignore error, this works
        self.queue_status = manager.Queue()  # ignore error, this works
        self.queue_results = manager.Queue()  # ignore error, this works

        self.provider = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                              queue_results=self.queue_results,
                                              queue_status=self.queue_status)

    def teardown(self):
        """Nose will run this method after every test method."""
        self.provider.release_all()

    def test_worker_process_provider_provision_once(self):
        """
        A worker process provider can provision a worker process.
        """
        self.provider.provision()

    def test_worker_process_provider_provision_repeated(self):
        """
        A worker process provider can provision multiple worker processes.
        """
        number_of_workers = 1
        for _ in range(1, 10):
            self.provider.provision(number_of_workers=number_of_workers)
            assert self.provider.worker_count == number_of_workers
            self.provider.release_all()

    @raises(IndexError)
    def test_worker_process_provider_provision_too_many(self):
        """
        A worker process provider can provision a limited number of workers.
        """
        # Try to provision a lot of workers.
        for number_of_workers in [_ ** _ for _ in range(0, 100)]:
            self.provider.provision(number_of_workers=number_of_workers)

    def test_worker_process_provider_provision_release_once(self):
        """
        A worker process provider can provision and release a worker process.
        """
        self.provider.provision()
        self.provider.release_all()

    def test_worker_process_provider_provision_release_twice(self):
        """
        A worker process provider can provide a worker process repeatedly.
        """
        # once
        self.provider.provision()
        self.provider.release_all()

        # and once more
        self.provider.provision()
        self.provider.release_all()

    def test_worker_process_provider_initializes_count(self):
        """A worker process provider begins to count at 0."""
        assert self.provider.worker_count == 0

    def test_worker_process_provider_counts_up(self):
        """A worker process provider counts in increments of 1."""
        # once
        self.provider.provision(1)
        assert self.provider.worker_count == 1

    def test_worker_process_provider_counts_up_down(self):
        """A worker process provider counts up and down."""
        self.provider.provision(1)
        assert self.provider.worker_count == 1
        self.provider.release_all()
        assert self.provider.worker_count == 0

    def test_worker_process_provider_counts_up_down_twice(self):
        """A worker process provider counts up and down repeatedly."""
        # once
        self.provider.provision(1)
        assert self.provider.worker_count == 1
        self.provider.release_all()
        assert self.provider.worker_count == 0

        # and once more
        self.provider.provision(1)
        assert self.provider.worker_count == 1
        self.provider.release_all()
        assert self.provider.worker_count == 0

    def test_worker_process_provider_is_borg(self):
        """There can only be one instance of a worker process provider."""
        my_provider = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                            queue_results=self.queue_results,
                                            queue_status=self.queue_status)

        number_of_workers = 1

        # left
        self.provider.provision(number_of_workers=number_of_workers)
        assert self.provider.worker_count == number_of_workers
        assert self.provider.worker_count == my_provider.worker_count

        # right
        my_provider.provision(number_of_workers=number_of_workers)
        assert self.provider.worker_count == number_of_workers * 2
        assert self.provider.worker_count == my_provider.worker_count

    def test_worker_process_provider_provision_and_stop_multiple_workers(self):
        """Workers can be provisioned and released repeatedly."""
        worker_count = 2  # any number more than one proves the point

        # once
        self.provider.provision(number_of_workers=worker_count)
        self.provider.release_all()

        # and once more
        self.provider.provision(number_of_workers=worker_count)
        self.provider.release_all()

if __name__ == '__main__':
    nose.runmodule()
