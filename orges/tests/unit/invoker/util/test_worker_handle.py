"""
Test for the worker handle utility.
"""
from __future__ import division, print_function, with_statement

from multiprocessing import Manager

from nose.tools.nontrivial import raises

from orges.util.stoppable import Stoppable, StoppedException
from orges.invoker.util.worker_provider import WorkerProcessHandle, \
    WorkerProcessProvider


def test_WorkerProcessHandle_inherits_stoppable():
    assert issubclass(WorkerProcessHandle, Stoppable)


def test_WorkerProcessHandle_is_stoppable():
    manager = Manager()
    worker_process_handle = WorkerProcessProvider().\
            provision(queue_tasks=manager.Queue(),
                      queue_results=manager.Queue(),
                      queue_status=manager.Queue())
    worker_process_handle.stop()


@raises(StoppedException)
def test_WorkerProcessHandle_is_stoppable_only_once():
    manager = Manager()
    worker_process_handle = WorkerProcessProvider().\
            provision(queue_tasks=manager.Queue(),
                      queue_results=manager.Queue(),
                      queue_status=manager.Queue())
    worker_process_handle.stop()  # first time should work
    worker_process_handle.stop()  # second time should fail
