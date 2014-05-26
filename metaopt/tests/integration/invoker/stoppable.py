# -*- coding: utf-8 -*-
"""
Tests for the pluggable invoker.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from nose.tools.nontrivial import raises
from nose.tools.trivial import eq_

# First Party
from metaopt.concurrent.invoker.invoker import Invoker
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.stoppable.util.exception import StoppedError
from metaopt.objective.integer.fast.implicit.f import f


f = f  # helps static code checkers identify attributes.


class TestStoppableInvoker(object):
    def test_instanciation(self):
        stoppable_invoker = Invoker()
        stoppable_invoker.f = f
        assert not stoppable_invoker.stopped
        stoppable_invoker.stop()
        assert stoppable_invoker.stopped

    @raises(StoppedError)
    def test_repeated_stop_raises_exception(self):
        stoppable_invoker = Invoker()
        stoppable_invoker.f = f
        stoppable_invoker.stop()
        stoppable_invoker.stop()

    def test_invoke(self):
        stoppable_invoker = Invoker()
        stoppable_invoker.f = f
        args = ArgsCreator(f.param_spec).args()
        eq_(stoppable_invoker.invoke(None, args), None)

    @raises(StoppedError)
    def test_invoke_raises_exception_when_stopped(self):
        stoppable_invoker = Invoker()
        stoppable_invoker.f = f
        args = ArgsCreator(f.param_spec).args()
        eq_(stoppable_invoker.invoke(None, args), None)
        stoppable_invoker.stop()
        eq_(stoppable_invoker.invoke(None, args), None)


if __name__ == '__main__':
    nose.runmodule()
