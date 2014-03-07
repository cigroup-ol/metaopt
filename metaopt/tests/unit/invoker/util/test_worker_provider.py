"""
Tests for the MutliProcess utilities.
"""
from __future__ import division, print_function, with_statement

from multiprocessing import Manager

import nose

from metaopt.invoker.util.worker_provider import WorkerProcessProvider


def test_WorkerProcessProvider_acts_as_singleton():
    manager = Manager()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    queue_results = manager.Queue()

    wpp0 = WorkerProcessProvider(queue_tasks=queue_tasks,
                                 queue_results=queue_results,
                                 queue_status=queue_status)
    wpp1 = WorkerProcessProvider(queue_tasks=queue_tasks,
                                 queue_results=queue_results,
                                 queue_status=queue_status)

    assert wpp0 is wpp1


def test_WorkerProcessProvider_provision_and_stop_single_worker():
    manager = Manager()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    queue_results = manager.Queue()

    worker_provider = WorkerProcessProvider(queue_tasks=queue_tasks,
                                 queue_results=queue_results,
                                 queue_status=queue_status)

    # once
    worker_provider.provision()
    worker_provider.release_all()

    # and once more
    worker_provider.provision()
    worker_provider.release_all()


def test_WorkerProcessProvider_provision_and_stop_multiple_workers():
    manager = Manager()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    queue_results = manager.Queue()

    worker_count = 2

    worker_provider = WorkerProcessProvider(queue_tasks=queue_tasks,
                                 queue_results=queue_results,
                                 queue_status=queue_status)

    # once
    worker_provider.provision(number_of_workers=worker_count)
    worker_provider.release_all()

    # and once more
    worker_provider.provision(number_of_workers=worker_count)
    worker_provider.release_all()

if __name__ == '__main__':
    nose.runmodule()
