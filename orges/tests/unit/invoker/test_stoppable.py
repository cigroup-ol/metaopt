"""
Tests for the pluggable invoker.
"""

from __future__ import division, print_function, with_statement

from nose.tools.trivial import eq_
from nose.tools.nontrivial import raises

from orges.core.args import ArgsCreator
from orges.util.stoppable import StoppedException
from orges.invoker.stoppable import StoppableInvoker
from orges.tests.util.functions import f

f = f  # helps static code checkers identify attributes.


def test_instanciation():
    stoppable_invoker = StoppableInvoker()
    assert not stoppable_invoker.stopped
    stoppable_invoker.stop()
    assert stoppable_invoker.stopped


@raises(StoppedException)
def test_repeated_stop_raises_exception():
    stoppable_invoker = StoppableInvoker()
    stoppable_invoker.stop()
    stoppable_invoker.stop()


def test_invoke():
    stoppable_invoker = StoppableInvoker()
    args = ArgsCreator(f.param_spec).args()
    eq_(stoppable_invoker.invoke(f, args), None)


@raises(StoppedException)
def test_invoke_raises_exception_when_stopped():
    stoppable_invoker = StoppableInvoker()
    args = ArgsCreator(f.param_spec).args()
    eq_(stoppable_invoker.invoke(f, args), None)
    stoppable_invoker.stop()
    eq_(stoppable_invoker.invoke(f, args), None)


if __name__ == '__main__':
    import nose
    nose.runmodule()
