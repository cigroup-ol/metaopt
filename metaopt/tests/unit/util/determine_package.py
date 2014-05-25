# -*- coding: utf-8 -*-
"""
Tests for the determine_package utility.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import string

# Third Party
import nose
from nose.tools.trivial import eq_

# First Party
from metaopt.concurrent.invoker.util.determine_package import determine_package
from metaopt.objective.integer.fast import FUNCTIONS_FAST


def local_function():
    """Stub function that is located in the same package of the tests."""
    pass


class LocalClass(object):
    """Stub class as determination target."""

    def local_method(self):
        """Stub method as determination target."""
        pass

    def foo_method(self):
        """Stub method as determination target."""
        pass

    def bar_method(self):
        """Stub method as determination target."""
        pass


class TestDeterminePackage(object):
    """Tests for the determine package utility."""

    def __init__(self):
        self._package_local_class = None
        self._package_local_method = None
        self._package_local_function = None

    def setup(self):
        """Nose will run this method before every test method."""
        self._package_local_function = determine_package(local_function)
        self._package_local_class = determine_package(LocalClass)
        self._package_local_method = determine_package(LocalClass.local_method)

    def teardown(self):
        """Nose will run this method after every test method."""
        pass

    def test_determine_local_function(self):
        eq_(self._package_local_function,
            "metaopt.tests.unit.util.determine_package")

        __import__(name=self._package_local_function, globals=globals(),
                   locals=locals(), fromlist=())

    def test_determine_local_class(self):
        eq_(self._package_local_class,
            "metaopt.tests.unit.util.determine_package")

        __import__(name=self._package_local_class, globals=globals(),
                   locals=locals(), fromlist=())

    def test_determine_local_method(self):
        eq_(self._package_local_method,
            "metaopt.tests.unit.util.determine_package")

        __import__(name=self._package_local_method, globals=globals(),
                   locals=locals(), fromlist=())

    def test_determine_imported(self):
        for index, function in enumerate(FUNCTIONS_FAST):
            package_remote_function = determine_package(function)
            a = "metaopt.objective.integer.fast.explicit." + \
                 string.ascii_lowercase[5 + index]
            b = "metaopt.objective.integer.fast.implicit." + \
                string.ascii_lowercase[3 + index]
            assert package_remote_function == a or \
                package_remote_function == b

            __import__(name=package_remote_function, globals=globals(),
                   locals=locals(), fromlist=())

if __name__ == '__main__':
    nose.runmodule()
