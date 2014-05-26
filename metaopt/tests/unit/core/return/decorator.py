# -*- coding: utf-8 -*-
"""
Test for returns module
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose

# First Party
from metaopt.core.returnspec.util.decorator import maximize, minimize


class TestDecorators(object):

    def test_maximize_creates_return_spec(self):
        @maximize("y")
        def f():
            pass

        assert "y" == f.return_spec.return_values[0]["name"]

    def test_minimize_creates_return_spec(self):
        @minimize("y")
        def f():
            pass

        assert "y" == f.return_spec.return_values[0]["name"]

if __name__ == '__main__':
    nose.runmodule()
