# -!- coding: utf-8 -!-
"""
Test for ReturnSpc
"""
from __future__ import division, print_function, with_statement

from nose.tools import raises

from orges.core.returnspec import ReturnSpec, ReturnValuesWrapper, \
    MultiObjectivesNotSupportedError


def test_return_spec_maximize():
    return_spec = ReturnSpec()
    return_spec.maximize("y")

    returned_values = ReturnValuesWrapper(return_spec, 1)
    other_returned_values = ReturnValuesWrapper(return_spec, 2)

    assert returned_values > other_returned_values

def test_return_spec_minimize():
    return_spec = ReturnSpec()
    return_spec.minimize("y")

    returned_values = ReturnValuesWrapper(return_spec, 1)
    other_returned_values = ReturnValuesWrapper(return_spec, 2)

    assert returned_values < other_returned_values

@raises(MultiObjectivesNotSupportedError)
def test_return_spec_multiple_objective_raises_error():
    return_spec = ReturnSpec()
    return_spec.minimize("y")
    return_spec.minimize("z")

def test_return_spec_given_function_create_default_return_values():
    def f(a):
        return a

    return_spec = ReturnSpec(f)

    assert return_spec.return_values[0]["name"] == "Fitness"


if __name__ == '__main__':
    import nose
    nose.runmodule()
