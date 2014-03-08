"""
Tests for the worker process utility.
"""

from __future__ import division, print_function, with_statement

import multiprocessing
import uuid
from multiprocessing import Manager
from multiprocessing.process import Process

import nose

from metaopt.core.args import ArgsCreator
from metaopt.invoker.util.determine_package import determine_package
from metaopt.invoker.util.model import Result, Start, Task
from metaopt.invoker.util.worker import Worker, WorkerProcess
from metaopt.tests.util.functions import FUNCTIONS_INTEGER_WORKING


def test_instanciation():
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    del worker_process


def test_superclasses():
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    isinstance(worker_process, Process)
    isinstance(worker_process, Worker)


def test_properties_return_instanciation_values():
    worker_id = uuid.uuid4()
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=worker_id,
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    assert worker_process.worker_id is worker_id


def test_initialization_is_sane():
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    assert worker_process.worker_id is not None


def test_start_terminate():
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_notask_terminate():
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_terminate():
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()
    queue_tasks.put(Task(id=uuid.uuid4,
                         function=determine_package(FUNCTIONS_INTEGER_WORKING[0]),
                         args=None, param_spec=None, return_spec=None,
                         kwargs=None))
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_attribute_terminate():
    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()
    queue_tasks.put(Task(id=uuid.uuid4,
                         function=determine_package(FUNCTIONS_INTEGER_WORKING[0]),
                         args=None, param_spec=None, return_spec=None,
                         kwargs=None))
    queue_status.get()
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_status_results_terminate():
    """
    Tests that a worker process correctly reports its start and result.

    This test uses all available functions.
    """

    manager = Manager()
    queue_results = manager.Queue()  # ignore error, this actually works.
    queue_tasks = manager.Queue()  # ignore error, this actually works.
    queue_status = manager.Queue()  # ignore error, this actually works.
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()

    for function in FUNCTIONS_INTEGER_WORKING:
        # log
        print(function)

        # send task to worker process
        task = Task(id=uuid.uuid4,
                    function=determine_package(function),
                    args=ArgsCreator(function.param_spec).args(),
                    param_spec=None, return_spec=None,
                    kwargs=None)
        queue_tasks.put(task)

        # check results
        status = queue_status.get()
        assert status
        assert isinstance(status, Start)
        result = queue_results.get()
        assert result
        assert isinstance(result, Result)

    # tear down
    worker_process.terminate()
    worker_process.join()

    # check postcondition
    assert not worker_process.is_alive()

if __name__ == '__main__':
    nose.runmodule()
