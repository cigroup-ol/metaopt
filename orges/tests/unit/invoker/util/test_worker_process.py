"""
Tests for the worker process utility.
"""

from __future__ import division, print_function, with_statement

import uuid
import logging
import multiprocessing
from multiprocessing import Manager
from multiprocessing.process import Process

import nose
from nose.tools.trivial import eq_
from nose.tools.nontrivial import raises

from orges.core.args import ArgsCreator
from orges.invoker.util.worker_provider import Task, Result, Status, Worker, \
    WorkerProcess
from orges.tests.util.integer_functions import INTEGER_FUNCTIONS
from orges.invoker.util.determine_package import determine_package


def _no_nose_setup():
    manager = Manager()
    worker_process = WorkerProcess(worker_id=uuid.uuid4(),
                                   queue_results=manager.Queue(),
                                   queue_status=manager.Queue(),
                                   queue_tasks=manager.Queue())
    return worker_process


def test_instanciation():
    _no_nose_setup()


def test_superclasses():
    worker_process = _no_nose_setup()
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
    worker_process = _no_nose_setup()
    assert not worker_process.current_task_id
    assert not worker_process.busy


def test_start_terminate():
    worker_process = _no_nose_setup()
    worker_process.start()
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_notask_terminate():
    worker_process = _no_nose_setup()
    worker_process.start()
    worker_process.queue_tasks.put(None)
    worker_process.terminate()
    worker_process.join()
    assert not worker_process.is_alive()


def test_start_task_terminate():
    worker_process = _no_nose_setup()
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

    for function in INTEGER_FUNCTIONS:
        # log
        print(function)

        # send task to worker process
        worker_process = _no_nose_setup()
        worker_process.start()
        worker_process.queue_tasks.put(Task(task_id=uuid.uuid4,
                                            function=determine_package(function),
                                            args=ArgsCreator(function.param_spec).args(),
                                            vargs=None,
                                            kwargs=None))
        #worker_process.queue_tasks.close()

        # check results
        status = worker_process.queue_status.get()
        #worker_process.queue_status.close()
        assert status
        assert isinstance(status, Status)
        result = worker_process.queue_results.get()
        #worker_process.queue_results.close()
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