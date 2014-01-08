"""
Tests for the MutliProcess utilities.
"""
from __future__ import division, print_function, with_statement

from multiprocessing import Manager

import nose
from nose.tools.nontrivial import raises

from orges.util.stoppable import Stoppable, StoppedException
from orges.invoker.util.worker_provider import WorkerProcessHandle, \
    WorkerProcessProvider


def test_WorkerProcessProvider_acts_as_singleton():
    wpp0, wpp1 = WorkerProcessProvider(), WorkerProcessProvider()

    assert wpp0 is wpp1


def test_WorkerProcessProvider_provision_and_stop():
    queue_tasks = Manager().Queue()
    queue_status = Manager().Queue()
    queue_results = Manager().Queue()

    worker_count = 2

    worker_provider = WorkerProcessProvider()

    # once
    workers = worker_provider.provision(number_of_workers=worker_count,
                                        queue_tasks=queue_tasks,
                                        queue_results=queue_results,
                                        queue_status=queue_status)
    for worker in workers:
        worker.stop()

    # and once more
    workers = worker_provider.provision(number_of_workers=worker_count,
                                        queue_tasks=queue_tasks,
                                        queue_results=queue_results,
                                        queue_status=queue_status)
    for worker in workers:
        worker.stop()


def test_WorkerHandle_inherits_stoppable():
    assert issubclass(WorkerProcessHandle, Stoppable)


def test_WorkerHandle_is_stoppable():
    queue_tasks = Manager().Queue()
    queue_status = Manager().Queue()
    queue_results = Manager().Queue()
    worker_process_handle = WorkerProcessProvider().\
            provision(queue_tasks, queue_results, queue_status)
    worker_process_handle.stop()


@raises(StoppedException)
def test_WorkerHandle_is_stoppable_only_once():
    queue_tasks = Manager().Queue()
    queue_status = Manager().Queue()
    queue_results = Manager().Queue()
    worker_process_handle = WorkerProcessProvider().\
            provision(queue_tasks, queue_results, queue_status)
    worker_process_handle.stop()  # first time should work
    worker_process_handle.stop()  # second time should fail

if __name__ == '__main__':
    nose.runmodule()
