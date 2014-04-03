"""
Tests for the worker process.
"""

from __future__ import division, print_function, with_statement

import uuid
from multiprocessing import Manager
from multiprocessing.process import Process

import nose
from nose.tools.nontrivial import raises

from metaopt.invoker.util.determine_package import determine_package
from metaopt.invoker.util.model import Error, Result, Start, Task
from metaopt.invoker.util.worker import Worker, WorkerProcess
from metaopt.tests.util.function.integer.fast import FUNCTIONS_FAST


class TestWorkerProcess(object):
    """Tests for the worker process."""

    def __init__(self):
        self.queue_outcome = None
        self.queue_status = None
        self.queue_tasks = None
        self.worker_process = None

    def setup(self):
        """Nose will run this method before every test method."""

        manager = Manager()
        self.queue_tasks = manager.Queue()  # ignore error, this works
        self.queue_status = manager.Queue()  # ignore error, this works
        self.queue_outcome = manager.Queue()  # ignore error, this works

        worker_id = uuid.uuid4()
        self.worker_process = WorkerProcess(worker_id=worker_id,
                                            queue_outcome=self.queue_outcome,
                                            queue_status=self.queue_status,
                                            queue_tasks=self.queue_tasks)
        self.worker_process.start()

    def teardown(self):
        """Nose will run this method after every test method."""

        if self.worker_process.is_alive():
            self.worker_process.terminate()
            self.worker_process.join()
        # check postcondition
        assert not self.worker_process.is_alive()

    def test_worker_inheritance(self):
        """Tests that is worker process is a worker."""

        isinstance(self.worker_process, Worker)

    def test_process_inheritance(self):
        """Tests that is worker process is a process."""

        isinstance(self.worker_process, Process)

    def test_worker_id_property_gets_intialized(self):
        assert self.worker_process.worker_id is not None

    def test_worker_process_is_alive(self):
        """Tests that a started worker process is alive."""

        assert self.worker_process.is_alive()

    @raises(AssertionError)
    def test_worker_process_started(self):
        """Tests that a started worker process cannot be started again."""

        self.worker_process.start()

    def test_worker_process_join(self):
        """Tests that joining an alive worker process times out."""

        self.worker_process.join(timeout=1)
        assert self.worker_process.is_alive()

    def test_worker_process_terminate_join(self):
        """Tests that terminating and joining a worker process kills it."""

        self.worker_process.terminate()
        self.worker_process.join()
        assert not self.worker_process.is_alive()

    def test_worker_process_start_task(self):
        """Tests that issuing task works does not raise an exception."""

        function = determine_package(FUNCTIONS_FAST[0])
        task_id = uuid.uuid4()
        self.queue_tasks.put(Task(id=task_id, function=function, args=None,
                                  kwargs=None))

    def test_worker_process_start_task_status_repeated(self):
        """
        Tests that a worker process reports its start.

        This method tests with all working integer functions.
        """

        for function in FUNCTIONS_FAST:
            # log
            print(function)

            # run
            function = determine_package(function)
            task_id = uuid.uuid4()
            task = Task(id=task_id, function=function, args=None, kwargs=None)
            self.queue_tasks.put(task)

            # check status
            status = self.queue_status.get()
            assert status
            assert isinstance(status, Start)
            assert status.worker_id == self.worker_process.worker_id
            assert status.task.id == task_id

    def test_worker_process_start_task_status_outcome_repeated(self):
        """
        Tests that a worker process reports its start and outcome.

        This method tests with all working integer functions.
        """

        for function in FUNCTIONS_FAST:
            # log
            print(function)

            # run
            function = determine_package(function)
            task_id = uuid.uuid4()
            task = Task(id=task_id, function=function, args=None, kwargs=None)
            self.queue_tasks.put(task)

            # check status
            status = self.queue_status.get()
            assert status
            assert isinstance(status, Start)
            assert status.worker_id == self.worker_process.worker_id
            assert status.task.id == task_id

            # check outcome
            outcome = self.queue_outcome.get()
            assert outcome

            # TODO avoid Errors
            #print(outcome)
            assert isinstance(outcome, Result) or isinstance(outcome, Error)
            #assert isinstance(outcome, Result)

            assert outcome.worker_id == self.worker_process.worker_id
            assert outcome.task.id == task_id

if __name__ == '__main__':
    nose.runmodule()
