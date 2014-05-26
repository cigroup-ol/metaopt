# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.returnspec.util.wrapper import ReturnValuesWrapper


def wrap_return_values(values, return_spec=None):
    return ReturnValuesWrapper(return_spec, values)
