# -*- coding: utf-8 -*-
"""
Tests for the Call Database which keeps track of task worker relations.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from multiprocessing.dummy import Manager
from uuid import uuid4

# Third Party
import nose
from nose.tools.nontrivial import raises

# First Party
from metaopt.concurrent.invoker.util.status_db import StatusDB
from metaopt.concurrent.model.call_lifecycle import Call, Result, Start
from metaopt.objective.integer.fast.explicit.f import f


# TODO test all stages of the call life cycle


class TestStatusDB(object):
    """
    Tests for the Call Database which keeps track of task worker relations.
    """

    def __init__(self):
        self._queue_outcome = None
        self._queue_task = None
        self._queue_start = None
        self._status_db = None

    def setup(self):
        """Nose executes this method before each test."""
        manager = Manager()
        self._queue_task = manager.Queue()
        self._queue_start = manager.Queue()
        self._queue_outcome = manager.Queue()
        self._status_db = StatusDB(queue_task=self._queue_task,
                                   queue_start=self._queue_start,
                                   queue_outcome=self._queue_outcome)

    def teardown(self):
        """Nose executes this method after each test."""
        pass

    def test_handle_status_start_once(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

    def test_handle_status_start_duplicate_is_silent(self):
        """Duplicate starts are handled quietly and do not issue errors."""
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        # once
        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        # once again
        # will raise error because issuing the same task twice makes no sense
        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

    @raises(ValueError)
    def test_handle_status_start_result_duplicate_raises(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        value = None
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        # once
        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)
        # once again
        worker_id = uuid4()
        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)

        # will work
        _ = self._status_db.wait_for_one_outcome()
        # will error because it makes no sense to issue the same task twice
        _ = self._status_db.wait_for_one_outcome()

    def test_handle_status_start_wait(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        self._queue_start.put(start)
        self._status_db.wait_for_one_start()

    def test_handle_status_increments_active_tasks_upon_start_once(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()
        count_tasks = self._status_db.count_running_tasks()

        assert count_tasks == 1

    def test_handle_status_increments_active_tasks_upon_start_twice(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        call_id = uuid4()
        call1 = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start1 = Start(worker_id=worker_id, call=call1)

        # once
        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        # twice
        self._queue_start.put(start1)
        _ = self._status_db.wait_for_one_start()

        count_tasks = self._status_db.count_running_tasks()
        assert count_tasks == 2

    @raises(KeyError)
    def test_handle_status_passes_outcome_of_immediate_result(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        args = None
        kwargs = None
        value = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)

        # there is no task that could have been finished
        # so a key error is risen
        _ = self._status_db.wait_for_one_outcome()

    def test_handle_status_passes_outcome_of_result_following_start(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        value = None
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)
        outcome = self._status_db.wait_for_one_outcome()

        assert isinstance(outcome, Result)
        assert outcome is result

    def test_handle_status_decrements_active_tasks_upon_result_once(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        value = None
        args = None
        kwargs = None
        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)

        start = Start(worker_id=worker_id, call=call)
        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)
        _ = self._status_db.wait_for_one_outcome()

        count_tasks = self._status_db.count_running_tasks()

        assert count_tasks == 0

    def test_handle_status_decrements_active_tasks_upon_result_twice(self):
        worker_id = uuid4()
        function = f
        value = None
        args = None
        kwargs = None

        call = Call(id=uuid4(), function=function, args=args, kwargs=kwargs)
        start = Start(worker_id=worker_id, call=call)

        call1 = Call(id=uuid4(), function=function, args=args, kwargs=kwargs)
        start1 = Start(worker_id=worker_id, call=call1)

        # once
        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)
        _ = self._status_db.wait_for_one_outcome()

        # twice
        self._queue_start.put(start1)
        _ = self._status_db.wait_for_one_start()

        result1 = Result(worker_id=worker_id, call=call1, value=value)
        self._queue_outcome.put(result1)
        _ = self._status_db.wait_for_one_outcome()

        # make assertions
        count_tasks = self._status_db.count_running_tasks()
        assert count_tasks == 0

    def test_handle_outcome_start_result_once(self):
        worker_id = uuid4()
        call_id = uuid4()
        function = f
        value = None
        args = None
        kwargs = None

        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)

        start = Start(worker_id=worker_id, call=call)
        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)
        _ = self._status_db.wait_for_one_outcome()

    @raises(ValueError)
    def test_handle_outcome_start_result_twice(self):
        call_id = uuid4()
        function = f
        args = None
        kwargs = None
        call = Call(id=call_id, function=function, args=args, kwargs=kwargs)

        value = None

        worker_id = uuid4()
        start = Start(worker_id=worker_id, call=call)
        self._queue_start.put(start)
        _ = self._status_db.wait_for_one_start()

        # once
        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)
        _ = self._status_db.wait_for_one_outcome()

        # twice
        worker_id = uuid4()
        result = Result(worker_id=worker_id, call=call, value=value)
        self._queue_outcome.put(result)
        _ = self._status_db.wait_for_one_outcome()

if __name__ == "__main__":
    nose.runmodule()
