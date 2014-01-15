"""
Tests for the worker process utility.
"""

from __future__ import division, print_function, with_statement

import uuid
import multiprocessing
from multiprocessing import Manager
from multiprocessing.process import Process

import nose

from orges.core.args import ArgsCreator
from orges.tests.util.functions import FUNCTIONS_INTEGER_WORKING
from orges.invoker.util.determine_package import determine_package
from orges.invoker.util.worker import WorkerProcess, Worker
from orges.invoker.util.model import Task, Status, Result


def get_default_worker_process():
    """Returns a worker process with attached queues and set worker id."""
    manager = Manager()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=manager.Queue(),
                                   queue_status=manager.Queue(),
                                   queue_tasks=manager.Queue())
    return worker_process


def test_instanciation():
    get_default_worker_process()


def test_superclasses():
    worker_process = get_default_worker_process()
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
    assert worker_process.queue_results is queue_results
    assert worker_process.queue_status is queue_status
    assert worker_process.queue_tasks is queue_tasks
    assert worker_process.worker_id is worker_id


def test_initialization_is_sane():
    worker_process = get_default_worker_process()
    assert not worker_process.current_task_id
    assert not worker_process.busy


def test_start_terminate():
    worker_process = get_default_worker_process()
    worker_process.start()
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_notask_terminate():
    worker_process = get_default_worker_process()
    worker_process.start()
    worker_process.queue_tasks.put(None)
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_terminate():
    worker_process = get_default_worker_process()
    worker_process.start()
    worker_process.queue_tasks.put(Task(task_id=uuid.uuid4,
                                        function=print,
                                        args=None,
                                        vargs=None,
                                        kwargs=None))
    worker_process.queue_tasks.put(None)
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_status_results_terminate():
    #multiprocessing.log_to_stderr()
    #logger = multiprocessing.get_logger()
    #logger.setLevel(logging.DEBUG)

    for function in FUNCTIONS_INTEGER_WORKING:
        # log
        print(function)

        # send task to worker process
        worker_process = get_default_worker_process()
        worker_process.start()
        task = Task(task_id=uuid.uuid4,
                    function=determine_package(function),
                    args=ArgsCreator(function.param_spec).args(),
                    vargs=None,
                    kwargs=None)
        worker_process.queue_tasks.put(task)

        # check results
        status = worker_process.queue_status.get()
        assert status
        assert isinstance(status, Status)
        result = worker_process.queue_results.get()
        assert result
        assert isinstance(result, Result)

        # tear down
        worker_process.terminate()
        worker_process.join()

        # check postcondition
        assert not worker_process.is_alive()
        assert not worker_process.current_task_id
        assert not worker_process.busy

if __name__ == '__main__':
    nose.runmodule()
