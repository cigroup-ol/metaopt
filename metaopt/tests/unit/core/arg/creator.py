# -*- coding: utf-8 -*-
"""
Tests for the creator module.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import itertools

# Third Party
import nose
from nose.tools import eq_

# First Party
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.objective.integer.fast import FUNCTIONS_FAST
from metaopt.objective.integer.fast.explicit import FUNCTIONS_FAST_EXPLICIT
from metaopt.tests.unit.core.arg.util. \
    get_intervals_from_function import get_intervals_from_function


try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3


class TestArgsCreator(object):
    def test_ArgsCreator_product_versus_itertools_product(self):
        for function in FUNCTIONS_FAST:
            # log
            print("next function: %s" % function.__module__)

            # mock
            intervals = get_intervals_from_function(function)
            valid_ranges = []
            for interval in intervals.values():
                start, stop = interval[0], interval[1]
                interval_range = xrange(start, stop + 1)  # [b, e) vs. [b, e]
                valid_ranges.append(interval_range)
            args_dummy = itertools.product(valid_ranges)
            for _ in args_dummy:
                pass  # forces execution of the range generators

            # TODO look for a better way to determine the number of params
            # than trying and failing.

            # use
            try:
                args_product = [(a.value, b.value)
                                for a, b in
                                ArgsCreator(function.param_spec).product()]
            except ValueError:
                args_product = [(a[0].value)
                                for a in
                                ArgsCreator(function.param_spec).product()]

            # compare
            for arg_p, arg_d in zip(args_product, args_dummy):
                eq_(arg_p[0], arg_d[0])
                eq_(arg_p[1], arg_d[1])

    def test_ArgsCreator_args_versus_nested_loop(self):
        for function in FUNCTIONS_FAST_EXPLICIT:
            # log
            print("next function: %s" % function.__module__)

            # mock
            intervals = get_intervals_from_function(function)

            args_dummy = []
            for x in intervals['x']:
                args_dummy.append(x)

                try:
                    for y in intervals['y']:
                        args_dummy.append(y)
                except KeyError:
                    pass

            # use
            args_args = ArgsCreator(function.param_spec).args()

            # compare
            for args, prod in zip(args_args, args_dummy):
                eq_(args.value, prod)

if __name__ == '__main__':
    nose.runmodule()
