"""
Tests for the singleton utility.
"""
from __future__ import division, print_function, with_statement

from metaopt.util.singleton import Singleton


class SingletonA(Singleton):
    """Mocks a singleton class."""
    def __init__(self):
        pass


class SingletonB(Singleton):
    """Mocks a singleton class."""
    def __init__(self):
        pass


class SingletonC(Singleton):
    """Mocks a singleton class."""
    common_knowledge = None

    def __init__(self, common_knowledge):
        self.common_knowledge = common_knowledge

    def report(self):
        return self.common_knowledge


class SingletonD(Singleton):
    """Mocks a singleton class."""
    def __init__(self, own_knowledge):
        self.own_knowledge = own_knowledge


def test_is():
    a_singleton, a2_singleton = SingletonA(), SingletonA()
    b_singleton, b2_singleton = SingletonB(), SingletonB()

    assert a_singleton is a2_singleton
    assert b_singleton is b2_singleton
    assert a_singleton is not b_singleton


def test_identity():
    a_singleton, a2_singleton = SingletonA(), SingletonA()
    b_singleton, b2_singleton = SingletonB(), SingletonB()

    assert id(a_singleton) == id(a2_singleton)
    assert id(b_singleton) == id(b2_singleton)
    assert id(a_singleton) is not id(b_singleton)


def test_borg_pattern():
    borg_0, borg_1 = SingletonC(42), SingletonC(None)

    assert borg_0.report() == borg_1.report()


def test_instance_attribute():
    instance_0, instance_1 = SingletonD(42), SingletonD(None)

    assert instance_0.own_knowledge == 42
    assert instance_0.own_knowledge == instance_1.own_knowledge

if __name__ == '__main__':
    import nose
    nose.runmodule()
