"""
Test for the Task Database that keeps track of task worker relations.
"""

from __future__ import division, print_function, with_statement

import nose

from metaopt.invoker.util.task_worker_db import TaskWorkerDB
from multiprocessing.dummy import Manager
from metaopt.invoker.util.model import Start, Result
from uuid import uuid4
from metaopt.tests.util.function.integer.working.f import f
from nose.tools.nontrivial import raises


manager = Manager()
queue_status = manager.Queue()
queue_outcome = manager.Queue()


def test_handle_status_start_once():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()


@raises(ValueError)
def test_handle_status_start_duplicate_raises():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    # once
    queue_status.put(start)
    _ = task_base.wait_for_one_status()
    # once again
    # will raise error because it makes no sense to issue the same task twice
    queue_status.put(start)
    _ = task_base.wait_for_one_status()


@raises(ValueError)
def test_handle_status_start_result_duplicate_raises():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    value = None
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    # once
    queue_outcome.put(result)
    # once again
    queue_outcome.put(result)

    # will work
    _ = task_base.wait_for_one_outcome()
    # will raise error because it makes no sense to issue the same task twice
    _ = task_base.wait_for_one_outcome()


def test_handle_status_passes_outcome_of_start():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    outcome = task_base.wait_for_one_status()

    assert isinstance(outcome, Start)
    assert outcome is start


def test_handle_status_increments_active_tasks_upon_start_once():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()
    count_tasks = task_base.count_running_tasks()

    assert count_tasks == 1


def test_handle_status_increments_active_tasks_upon_start_twice():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    # once
    worker_id = uuid4()
    task_id = uuid4()
    function = f
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    # twice
    worker_id = uuid4()
    task_id = uuid4()
    function = f
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    count_tasks = task_base.count_running_tasks()

    print(count_tasks)
    assert count_tasks == 2


@raises(KeyError)
def test_handle_status_passes_outcome_of_immediate_result():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    args = None
    kwargs = None
    value = None
    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    queue_outcome.put(result)

    # there is no task that could have been finished
    # so a key error is risen
    _ = task_base.wait_for_one_outcome()


def test_handle_status_passes_outcome_of_result_following_start():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    value=None
    args = None
    kwargs = None
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    queue_outcome.put(result)
    outcome = task_base.wait_for_one_outcome()

    assert isinstance(outcome, Result)
    assert outcome is result


def test_handle_status_decrements_active_tasks_upon_result_once():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    value = None
    args = None
    kwargs = None

    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    queue_outcome.put(result)
    _ = task_base.wait_for_one_outcome()

    count_tasks = task_base.count_running_tasks()

    assert count_tasks == 0


def test_handle_status_decrements_active_tasks_upon_result_twice():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    # once
    worker_id = uuid4()
    task_id = uuid4()
    function = f
    value = None
    args = None
    kwargs = None

    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    queue_outcome.put(result)
    _ = task_base.wait_for_one_outcome()

    # twice
    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    queue_outcome.put(result)
    _ = task_base.wait_for_one_outcome()

    count_tasks = task_base.count_running_tasks()

    assert count_tasks == 0


def test_handle_outcome_start_result_once():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    value = None
    args = None
    kwargs = None

    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    queue_outcome.put(result)
    _ = task_base.wait_for_one_outcome()


@raises(ValueError)
def test_handle_outcome_start_result_twice():
    task_base = TaskWorkerDB(queue_status=queue_status,
                         queue_outcome=queue_outcome)

    worker_id = uuid4()
    task_id = uuid4()
    function = f
    value = None
    args = None
    kwargs = None

    start = Start(worker_id=worker_id, task_id=task_id, function=function,
                  args=args, kwargs=kwargs)
    queue_status.put(start)
    _ = task_base.wait_for_one_status()

    result = Result(worker_id=worker_id, task_id=task_id, function=function,
                    value=value, args=args, kwargs=kwargs)
    # once
    queue_outcome.put(result)
    _ = task_base.wait_for_one_outcome()

    # twice
    queue_outcome.put(result)
    _ = task_base.wait_for_one_outcome()

if __name__ == "__main__":
    nose.runmodule()
