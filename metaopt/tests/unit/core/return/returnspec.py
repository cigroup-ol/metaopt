# -*- coding: utf-8 -*-
# -!- coding: utf-8 -!-
"""
Test for ReturnSpc
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from nose.tools import raises

# First Party
from metaopt.core.returnspec.returnspec import ReturnSpec
from metaopt.core.returnspec.util. \
    exception import MultiObjectivesNotSupportedError
from metaopt.core.returnspec.util.wrapper import ReturnValuesWrapper


class TestRetunspec(object):
    def test_return_spec_maximize(self):
        return_spec = ReturnSpec()
        return_spec.maximize("y")

        returned_values = ReturnValuesWrapper(return_spec, 1)
        other_returned_values = ReturnValuesWrapper(return_spec, 2)

        assert returned_values > other_returned_values

    def test_return_spec_minimize(self):
        return_spec = ReturnSpec()
        return_spec.minimize("y")

        returned_values = ReturnValuesWrapper(return_spec, 1)
        other_returned_values = ReturnValuesWrapper(return_spec, 2)

        assert returned_values < other_returned_values

    @raises(MultiObjectivesNotSupportedError)
    def test_return_spec_multiple_objective_raises_error(self):
        return_spec = ReturnSpec()
        return_spec.minimize("y")
        return_spec.minimize("z")

    def test_return_spec_given_function_create_default_return_values(self):
        def f(a):
            return a

        return_spec = ReturnSpec(f)

        assert return_spec.return_values[0]["name"] == "Fitness"
        assert return_spec.return_values[0]["minimize"] == True

    def test_is_minimization_without_return_spec(self):
        returned_values = ReturnValuesWrapper(None, 1)
        other_returned_values = ReturnValuesWrapper(None, 2)

        assert returned_values < other_returned_values

    def test_raw_values(self):
        returned_values = ReturnValuesWrapper(None, 1)
        assert returned_values.raw_values == 1

if __name__ == '__main__':
    nose.runmodule()
