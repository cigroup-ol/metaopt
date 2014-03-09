"""
Tests for the stoppable invoker.
"""

from __future__ import division, print_function, with_statement

import nose
from nose.tools.nontrivial import raises

from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.tests.util.functions import f
from metaopt.util.stoppable import StoppedException

f = f  # helps static code checkers identify attributes.


class TestMultiProcessInvoker(object):
    """"Tests for the multi-process invoker."""
    def __init__(self):
        pass

    def setup(self):
        self.invoker = MultiProcessInvoker()

    def teardown(self):
        del self.invoker

    def test_instanciation(self):
        pass

    def test_sane_initiation(self):
        assert not self.invoker.stopped

    def test_protected_attributes(self):
        self.invoker.f = f

        assert self.invoker._lock is not None
        assert self.invoker._queue_outcome is not None
        assert self.invoker._queue_status is not None
        assert self.invoker._queue_task is not None
        assert self.invoker._worker_count_max >= 1

    def test_stop(self):
        self.invoker.stop()
        assert self.invoker.stopped

    @raises(StoppedException)
    def test_repeated_stop_raises_exception(self):
        self.invoker.stop()
        self.invoker.stop()

    @raises(StoppedException)
    def test_invoke_raises_exception_when_stopped(self):
        self.invoker.stop()
        self.invoker.invoke()

if __name__ == '__main__':
    nose.runmodule()
