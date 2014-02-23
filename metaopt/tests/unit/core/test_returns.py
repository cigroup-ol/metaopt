"""
Test for returns module
"""
from __future__ import division, print_function, with_statement

from metaopt.core.returns import maximize, minimize


def test_maximize_creates_return_spec():
    @maximize("y")
    def f():
        pass

    assert "y" == f.return_spec.return_values[0]["name"]

def test_minimize_creates_return_spec():
    @minimize("y")
    def f():
        pass

    assert "y" == f.return_spec.return_values[0]["name"]

if __name__ == '__main__':
    import nose
    nose.runmodule()
