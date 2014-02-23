"""
Tests for the determine_package utility.
"""
from __future__ import division, print_function, with_statement

import string

import nose
from nose.tools.trivial import eq_

from metaopt.invoker.util.determine_package import determine_package
from metaopt.tests.util.functions import FUNCTIONS_INTEGER_WORKING


def local_function():
    """Stub function that is located in the same package of the tests."""
    pass


class LocalClass(object):
    """Stub class as determination target."""

    def local_method(self):
        """Stub method as determination target."""
        pass


def test_determine_local_function():
    eq_(determine_package(local_function),
        "metaopt.tests.unit.invoker.util.test_determine_package")


def test_determine_local_class():
    eq_(determine_package(LocalClass),
        "metaopt.tests.unit.invoker.util.test_determine_package")


def test_determine_local_method():
    eq_(determine_package(LocalClass.local_method),
        "metaopt.tests.unit.invoker.util.test_determine_package")


def test_determine_imported():
    for index, function in enumerate(FUNCTIONS_INTEGER_WORKING):
        eq_(determine_package(function),
           ("metaopt.tests.util.function.integer.working." +
            string.ascii_lowercase[5 + index]))

if __name__ == '__main__':
    nose.runmodule()
