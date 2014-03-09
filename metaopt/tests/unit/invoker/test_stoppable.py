"""
Tests for the pluggable invoker.
"""

from __future__ import division, print_function, with_statement

import nose
from nose.tools.nontrivial import raises
from nose.tools.trivial import eq_

from metaopt.core.args import ArgsCreator
from metaopt.invoker.stoppable import StoppableInvoker
from metaopt.tests.util.functions import f
from metaopt.util.stoppable import StoppedException

f = f  # helps static code checkers identify attributes.


def test_instanciation():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.f = f
    assert not stoppable_invoker.stopped
    stoppable_invoker.stop()
    assert stoppable_invoker.stopped


@raises(StoppedException)
def test_repeated_stop_raises_exception():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.f = f
    stoppable_invoker.stop()
    stoppable_invoker.stop()


def test_invoke():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.f = f
    args = ArgsCreator(f.param_spec).args()
    eq_(stoppable_invoker.invoke(None, args), None)


@raises(StoppedException)
def test_invoke_raises_exception_when_stopped():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.f = f
    args = ArgsCreator(f.param_spec).args()
    eq_(stoppable_invoker.invoke(None, args), None)
    stoppable_invoker.stop()
    eq_(stoppable_invoker.invoke(None, args), None)


if __name__ == '__main__':
    nose.runmodule()
