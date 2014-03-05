"""
Tests for the stoppable invoker.
"""

from __future__ import division, print_function, with_statement

from nose.tools.nontrivial import raises
from nose.tools.trivial import eq_

from metaopt.core.args import ArgsCreator
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.invoker.util.task_handle import TaskHandle
from metaopt.invoker.util.worker_provider import WorkerProcessProvider
from metaopt.tests.util.functions import f
from metaopt.util.stoppable import StoppedException

f = f  # helps static code checkers identify attributes.

StoppableInvoker = MultiProcessInvoker


def test_instanciation():
    stoppable_invoker = StoppableInvoker()
    del stoppable_invoker


def test_sane_initiation():
    stoppable_invoker = StoppableInvoker()
    assert not stoppable_invoker.stopped


def test_protected_attributes():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.f = f

    assert stoppable_invoker._lock is not None
    assert stoppable_invoker._queue_outcome is not None
    assert stoppable_invoker._queue_status is not None
    assert stoppable_invoker._queue_tasks is not None
    assert stoppable_invoker._worker_count_max >= 1
    assert isinstance(stoppable_invoker._worker_handles, list)
    assert isinstance(stoppable_invoker._worker_provider,
                      WorkerProcessProvider)


def test_stop():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.stop()
    assert stoppable_invoker.stopped


@raises(StoppedException)
def test_repeated_stop_raises_exception():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.stop()
    stoppable_invoker.stop()


def test_invoke():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.f = f
    args = ArgsCreator(f.param_spec).args()
    isinstance(stoppable_invoker.invoke(None, args), TaskHandle)


@raises(StoppedException)
def test_invoke_raises_exception_when_stopped():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.f = f
    args = ArgsCreator(f.param_spec).args()
    isinstance(stoppable_invoker.invoke(None, args), TaskHandle)
    stoppable_invoker.stop()
    eq_(stoppable_invoker.invoke(None, args), None)


# TODO test invoker behavior

if __name__ == '__main__':
    import nose
    nose.runmodule()
