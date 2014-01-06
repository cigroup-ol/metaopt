"""
Tests for the stoppable.
"""

from __future__ import division, print_function, with_statement

from nose.tools.nontrivial import raises

from orges.util.stoppable import Stoppable, StoppedException, stoppable_method


def test_stoppable_is_not_stopped_initially():
    stoppable = Stoppable()
    assert not stoppable.stopped


def test_stopping_is_itempotent():
    stoppable = Stoppable()
    assert not stoppable.stopped
    assert not stoppable.stopped


@raises(StoppedException)
def test_stopping_twice_raises_exception():
    stoppable = Stoppable()
    stoppable.stop()
    stoppable.stop()


def test_stoppablity():
    stoppable = Stoppable()
    stoppable.stop()
    assert stoppable.stopped


def test_stopping_is_idempotent():
    stoppable = Stoppable()
    stoppable.stop()
    assert stoppable.stopped
    assert stoppable.stopped


class MockStoppable(Stoppable):
    """Mock up Stoppable with a stoppable method."""

    @stoppable_method
    def run(self):
        """A method that does something."""
        pass  # no operation qualifies as "something"


def test_stoppable_decorator():
    mock_stoppable = MockStoppable()
    assert not mock_stoppable.stopped
    mock_stoppable.run()
    mock_stoppable.run()
    mock_stoppable.stop()
    assert mock_stoppable.stopped


@raises(StoppedException)
def test_stoppable_decorator_raises_exception_when_called_after_stopping():
    mock_stoppable = MockStoppable()
    mock_stoppable.run()
    mock_stoppable.run()
    mock_stoppable.stop()
    assert mock_stoppable.stopped
    mock_stoppable.run()

if __name__ == '__main__':
    import nose
    nose.runmodule()
