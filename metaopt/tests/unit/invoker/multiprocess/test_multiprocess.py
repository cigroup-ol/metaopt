"""
Tests for the stoppable invoker.
"""

from __future__ import division, print_function, with_statement

import nose
from nose.tools.nontrivial import raises
from nose.tools.trivial import eq_

from metaopt.core.args import ArgsCreator
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.invoker.util.task_handle import TaskHandle
from metaopt.invoker.util.worker_provider import WorkerProcessProvider
from metaopt.tests.util.functions import f
from metaopt.util.stoppable import StoppedException
from mock import Mock

f = f  # helps static code checkers identify attributes.


def test_instanciation():
    stoppable_invoker = MultiProcessInvoker()
    del stoppable_invoker


def test_sane_initiation():
    stoppable_invoker = MultiProcessInvoker()
    assert not stoppable_invoker.stopped


def test_protected_attributes():
    stoppable_invoker = MultiProcessInvoker()
    stoppable_invoker.f = f

    assert stoppable_invoker._lock is not None
    assert stoppable_invoker._queue_outcome is not None
    assert stoppable_invoker._queue_status is not None
    assert stoppable_invoker._queue_task is not None
    assert stoppable_invoker._worker_count_max >= 1
    assert isinstance(stoppable_invoker._worker_provider,
                      WorkerProcessProvider)


def test_stop():
    stoppable_invoker = MultiProcessInvoker()
    stoppable_invoker.stop()
    assert stoppable_invoker.stopped


@raises(StoppedException)
def test_repeated_stop_raises_exception():
    stoppable_invoker = MultiProcessInvoker()
    stoppable_invoker.stop()
    stoppable_invoker.stop()


@raises(StoppedException)
def test_invoke_raises_exception_when_stopped():
    invoker = MultiProcessInvoker()
    invoker.stop()
    invoker.invoke()


if __name__ == '__main__':
    nose.runmodule()
    #test_invoke()
