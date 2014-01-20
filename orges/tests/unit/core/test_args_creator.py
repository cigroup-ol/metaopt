# -*- coding: utf-8 -*-
"""
Tests for the ArgsCreator module.
"""

from __future__ import division, print_function, with_statement

import itertools

from nose.tools import eq_

from orges.core.args import ArgsCreator
from orges.tests.unit.core.util import get_intervals_from_function
from orges.tests.util.functions import FUNCTIONS_INTEGER_WORKING
from orges.invoker.util.determine_package import determine_package

try:
    xrange  # will work in python2, only
except NameError:
    xrange = range  # rename range to xrange in python3


def test_ArgsCreator_product_versus_itertools_product():
    for function in FUNCTIONS_INTEGER_WORKING:
        # log
        print(function)

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
        print(args_dummy)

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
        print(args_product)

        # compare
        for arg_p, arg_d in zip(args_product, args_dummy):
            eq_(arg_p[0], arg_d[0])
            eq_(arg_p[1], arg_d[1])


def test_ArgsCreator_args_versus_nested_loop():
    for function in FUNCTIONS_INTEGER_WORKING:
        # log
        print(function, determine_package(function))

        # mock
        intervals = get_intervals_from_function(function)

        args_dummy = []
        for a in intervals['a']:
            args_dummy.append(a)

            try:
                for b in intervals['b']:
                    args_dummy.append(b)
            except KeyError:
                pass

        # use
        args_args = ArgsCreator(function.param_spec).args()
        print(args_args)

        # compare
        for args, prod in zip(args_args, args_dummy):
            eq_(args.value, prod)

if __name__ == '__main__':
    import nose
    nose.runmodule()
