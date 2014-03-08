"""
Tests for the worker process provider.
"""
from __future__ import division, print_function, with_statement

from multiprocessing import Manager

import nose

from metaopt.invoker.util.worker_provider import WorkerProcessProvider


class TestWorkerProcess(object):
    def setup(self):
        manager = Manager()
        self.queue_tasks = manager.Queue()
        self.queue_status = manager.Queue()
        self.queue_results = manager.Queue()

    def teardown(self):
        pass

    def test_count(self):
        provider = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                         queue_results=self.queue_results,
                                         queue_status=self.queue_status)
        assert provider.worker_count() == 0

    def test_count_counts_once(self):
        provider = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                         queue_results=self.queue_results,
                                         queue_status=self.queue_status)

        # once
        provider.provision(1)
        assert provider.worker_count() == 1
        provider.release_all()
        assert provider.worker_count() == 0

    def test_count_counts_twice(self):
        provider = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                         queue_results=self.queue_results,
                                         queue_status=self.queue_status)

        # once
        provider.provision(1)
        assert provider.worker_count() == 1
        provider.release_all()
        assert provider.worker_count() == 0

        # and once more
        provider.provision(1)
        assert provider.worker_count() == 1
        provider.release_all()
        assert provider.worker_count() == 0

    def test_WorkerProcessProvider_acts_as_singleton(self):
        provider_0 = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                           queue_results=self.queue_results,
                                           queue_status=self.queue_status)
        provider_1 = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                           queue_results=self.queue_results,
                                           queue_status=self.queue_status)

        assert provider_0 is provider_1

    def test_WorkerProcessProvider_provision_and_stop_single_worker(self):
        provider = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                         queue_results=self.queue_results,
                                         queue_status=self.queue_status)

        # once
        provider.provision()
        provider.release_all()

        # and once more
        provider.provision()
        provider.release_all()

    def test_WorkerProcessProvider_provision_and_stop_multiple_workers(self):
        worker_count = 2  # any number more than one proves the point

        provider = WorkerProcessProvider(queue_tasks=self.queue_tasks,
                                         queue_results=self.queue_results,
                                         queue_status=self.queue_status)

        # once
        provider.provision(number_of_workers=worker_count)
        provider.release_all()

        # and once more
        provider.provision(number_of_workers=worker_count)
        provider.release_all()



if __name__ == '__main__':
    nose.runmodule()
