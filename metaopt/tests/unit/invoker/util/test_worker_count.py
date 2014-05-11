"""
Tests for the determine_package utility.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from multiprocessing import cpu_count

# Third Party
import nose
from nose.tools.nontrivial import raises

# First Party
from metaopt.invoker.util.determine_worker_count import determine_worker_count


def test_determine_worker_count():
    assert determine_worker_count() is cpu_count()


def test_determine_worker_count_none():
    assert determine_worker_count(request=None) >= 1


def test_determine_worker_count_named_param():
    assert determine_worker_count(request=None) >= 1


def test_determine_worker_count_one():
    assert determine_worker_count(request=1) is 1


@raises(NotImplementedError)
def test_determine_worker_count_no_core():
    determine_worker_count(request=0)


@raises(NotImplementedError)
def test_determine_worker_count_string():
    determine_worker_count(request="a")

if __name__ == '__main__':
    nose.runmodule()
