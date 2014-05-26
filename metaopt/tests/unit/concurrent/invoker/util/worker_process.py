# -*- coding: utf-8 -*-
"""
Tests for the worker process.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import uuid
from multiprocessing import Manager
from multiprocessing.process import Process

# Third Party
import nose
from nose.tools.nontrivial import raises

# First Party
from metaopt.concurrent.invoker.util.determine_package import determine_package
from metaopt.concurrent.model.call_lifecycle import Call, Error, Result, \
    Start, Task
from metaopt.concurrent.worker.process import ProcessWorker
from metaopt.concurrent.worker.worker import Worker
from metaopt.objective.integer.fast import FUNCTIONS_FAST


class TestWorkerProcess(object):
    """Tests for the worker process."""

    def __init__(self):
        self._queue_outcome = None
        self._queue_start = None
        self._queue_task = None
        self.worker_process = None

    def setup(self):
        """Nose will run this method before every test method."""

        manager = Manager()
        self._queue_task = manager.Queue()  # ignore error, this works
        self._queue_start = manager.Queue()  # ignore error, this works
        self._queue_outcome = manager.Queue()  # ignore error, this works

        self.worker_process = ProcessWorker(queue_outcome=self._queue_outcome,
                                            queue_start=self._queue_start,
                                            queue_tasks=self._queue_task)

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
        call_id = uuid.uuid4()
        self._queue_task.put(Task(call=Call(id=call_id, function=function,
                                            args=None, kwargs=None)))

    def test_worker_process_start_task_status_repeated(self):
        """
        Tests that a worker process reports its start.

        This method tests with all working integer functions.
        """

        for function in FUNCTIONS_FAST:
            # log
            print("next function: %s" % function.__module__)

            # run
            function = determine_package(function)
            call_id = uuid.uuid4()
            call = Call(id=call_id, function=function, args=None, kwargs=None)
            task = Task(call=call)
            self._queue_task.put(task)

            # check status
            start = self._queue_start.get()
            assert start
            assert isinstance(start, Start)
            assert start.worker_id == self.worker_process.worker_id
            assert start.call.id == call_id

    def test_worker_process_start_task_status_outcome_repeated(self):
        """
        Tests that a worker process reports its start and outcome.

        This method tests with all working integer functions.
        """

        for function in FUNCTIONS_FAST:
            # log
            print("next function: %s" % function.__module__)

            # run
            function = determine_package(function)
            call_id = uuid.uuid4()
            call = Call(id=call_id, function=function, args=None, kwargs=None)
            task = Task(call=call)
            self._queue_task.put(task)

            # check status
            status = self._queue_start.get()
            assert status
            assert isinstance(status, Start)
            assert status.worker_id == self.worker_process.worker_id
            assert status.call.id == call_id

            # check outcome
            outcome = self._queue_outcome.get()
            assert outcome

            # TODO avoid Errors
            #print(outcome)
            assert isinstance(outcome, Result) or isinstance(outcome, Error)
            #assert isinstance(outcome, Result)

            assert outcome.worker_id == self.worker_process.worker_id
            assert outcome.call.id == call_id

if __name__ == '__main__':
    nose.runmodule()
