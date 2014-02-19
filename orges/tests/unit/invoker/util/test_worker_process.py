"""
Tests for the worker process utility.
"""

from __future__ import division, print_function, with_statement

import multiprocessing
import uuid
from multiprocessing import Manager
from multiprocessing.process import Process

import nose

from orges.core.args import ArgsCreator
from orges.invoker.util.determine_package import determine_package
from orges.invoker.util.model import Finish, Result, Start, Task
from orges.invoker.util.worker import Worker, WorkerProcess
from orges.tests.util.functions import FUNCTIONS_INTEGER_WORKING


def test_instanciation():
    manager = Manager()
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    del worker_process


def test_superclasses():
    manager = Manager()
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    isinstance(worker_process, Process)
    isinstance(worker_process, Worker)


def test_properties_return_instanciation_values():
    worker_id = uuid.uuid4()
    queue_results = multiprocessing.Queue()
    queue_status = multiprocessing.Queue()
    queue_tasks = multiprocessing.Queue()
    worker_process = WorkerProcess(worker_id=worker_id,
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    assert worker_process.worker_id is worker_id


def test_initialization_is_sane():
    manager = Manager()
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    assert worker_process.worker_id is not None


def test_start_terminate():
    manager = Manager()
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
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
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()
    worker_process.queue_tasks.put(None)
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_terminate():
    manager = Manager()
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()
    queue_tasks.put(Task(task_id=uuid.uuid4,
                         function=determine_package(FUNCTIONS_INTEGER_WORKING[0]),
                         args=None,
                         kwargs=None))
    queue_tasks.put(None)
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_attribute_terminate():
    manager = Manager()
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()
    queue_tasks.put(Task(task_id=uuid.uuid4,
                                        function=determine_package(FUNCTIONS_INTEGER_WORKING[0]),
                                        args=None,
                                        kwargs=None))
    queue_tasks.put(None)
    queue_status.get()
    assert worker_process._current_task_id is not None
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_status_results_terminate():
    #multiprocessing.log_to_stderr()
    #logger = multiprocessing.get_logger()
    #logger.setLevel(logging.DEBUG)

    manager = Manager()
    queue_results = manager.Queue()
    queue_tasks = manager.Queue()
    queue_status = manager.Queue()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=queue_results,
                                   queue_status=queue_status,
                                   queue_tasks=queue_tasks)
    worker_process.start()

    for function in FUNCTIONS_INTEGER_WORKING:
        # log
        print(function)

        # send task to worker process
        task = Task(task_id=uuid.uuid4,
                    function=determine_package(function),
                    args=ArgsCreator(function.param_spec).args(),
                    kwargs=None)
        queue_tasks.put(task)

        # check results
        status = queue_status.get()
        assert status
        assert isinstance(status, Start) or isinstance(status, Finish)
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
