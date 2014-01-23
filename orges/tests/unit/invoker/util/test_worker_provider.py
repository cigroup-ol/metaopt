"""
Tests for the MutliProcess utilities.
"""
from __future__ import division, print_function, with_statement

from multiprocessing import Manager

import nose

from orges.invoker.util.worker_provider import WorkerProcessProvider


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
    worker = worker_provider.provision()
    worker.stop()

    # and once more
    worker = worker_provider.provision()
    worker.stop()


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
    workers = worker_provider.provision(number_of_workers=worker_count)
    for worker in workers:
        worker.stop()

    # and once more
    workers = worker_provider.provision(number_of_workers=worker_count)
    for worker in workers:
        worker.stop()

if __name__ == '__main__':
    nose.runmodule()
