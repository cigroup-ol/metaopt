"""
Tests the singleton utility.
"""
from __future__ import division, print_function, with_statement

from orges.util.singleton import Singleton


def test_singleton():
    class ASingleton(Singleton):
        """Mocks a singleton class."""
        def __init__(self):
            pass

    class BSingleton(Singleton):
        """Mocks a singleton class."""
        def __init__(self):
            pass

    a_singleton, a2_singleton = ASingleton(), ASingleton()
    b_singleton, b2_singleton = BSingleton(), BSingleton()

    assert a_singleton is a2_singleton
    assert b_singleton is b2_singleton
    assert a_singleton is not b_singleton

if __name__ == '__main__':
    import nose
    nose.runmodule()
