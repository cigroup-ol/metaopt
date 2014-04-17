"""
System tests for the custom optimize.
"""
from __future__ import division, print_function, with_statement

from itertools import product

import nose
from nose.tools import eq_

from metaopt.core.main import custom_optimize
from metaopt.invoker.dualthread import DualThreadInvoker
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.invoker.pluggable import PluggableInvoker
from metaopt.invoker.simple_multiprocess import SimpleMultiprocessInvoker
from metaopt.invoker.singleprocess import SingleProcessInvoker
from metaopt.invoker.stoppable import StoppableInvoker
from metaopt.invoker.util.import_function import import_function
from metaopt.optimizer.gridsearch import GridSearchOptimizer
from metaopt.optimizer.rechenberg import RechenbergOptimizer
from metaopt.optimizer.saes import SAESOptimizer
from metaopt.tests.util.function.integer.failing import FUNCTIONS_FAILING
from metaopt.tests.util.function.integer.fast. \
    explicit import FUNCTIONS_FAST_EXPLICIT
from metaopt.tests.util.function.integer.fast.explicit.f import f as f_max_fast
from metaopt.tests.util.function.integer.fast.explicit.g import f as f_min_fast
from metaopt.tests.util.function.integer.fast. \
    implicit import FUNCTIONS_FAST_IMPLICIT
from metaopt.tests.util.function.integer.slow.explicit.f import f as f_max_slow
from metaopt.tests.util.function.integer.slow.explicit.g import f as f_min_slow


class TestMain(object):

    def __init__(self):
        self._invokers = None
        self._optimizers = None

    def setup(self):
        self._invokers = [
            DualThreadInvoker,
            MultiProcessInvoker,
            #StoppableInvoker,  # TODO NotImplementedError
            #PluggableInvoker(DualThreadInvoker()), # TODO faulty result
            #PluggableInvoker(MultiProcessInvoker()),  # TODO on_error kwargs
            #SingleProcessInvoker(),  # TODO NotImplementedError
            #SimpleMultiprocessInvoker(), # TODO hanging
            ]
        self._optimizers = [
            GridSearchOptimizer,
            #SAESOptimizer(),  # TODO TypeError
            #RechenbergOptimizer(),  # TODO TypeError None is not iterable
            ]

    def teardown(self):
        del self._invokers
        del self._optimizers

    def _wrap(self, target):
        """
        Calls the given target method with all invokers and optimizers.
        """
        for invoker, optimizer in product(self._invokers, self._optimizers):
            print("next invoker: %s, next optimizer: %s" % \
                  (invoker.__name__, optimizer.__name__))
            optimizer = optimizer()
            invoker = invoker()
            target(invoker=invoker, optimizer=optimizer)
            del invoker, optimizer

    def test_custom_optimize_maximize(self):
        self._wrap(self._test_custom_optimize_maximize)

    def test_custom_optimize_minimize(self):
        self._wrap(self._test_custom_optimize_minimize)

    def test_custom_optimize_maximize_hang_global_timeout(self):
        self._wrap(self._test_custom_optimize_maximize_hang_global_timeout)

    def test_custom_optimize_minimize_hang_global_timeout(self):
        self._wrap(self._test_custom_optimize_minimize_hang_global_timeout)

    def test_function_fast(self):
        for test in [self._test_integer_fast_explicit,
                     self._test_integer_fast_implicit]:
            print("next test: %s" % test)
            self._wrap(test)

    def test_integer_failing(self):
        self._wrap(self._test_integer_failing)

    def _test_integer_failing(self, invoker, optimizer):
        for function in FUNCTIONS_FAILING:
            print("next function: %s" % function)
            self._test_function_failing(function, invoker=invoker,
                                        optimizer=optimizer)

    def _test_integer_fast_explicit(self, invoker, optimizer):
        for function in FUNCTIONS_FAST_EXPLICIT:
            print("next function: %s" % function)
            self._test_function_fast(function=function, invoker=invoker,
                                     optimizer=optimizer)

    def _test_integer_fast_implicit(self, invoker, optimizer):
        for function in FUNCTIONS_FAST_IMPLICIT:
            print("next function: %s" % function)
            self._test_function_fast(function=function, invoker=invoker,
                                     optimizer=optimizer)

    def _test_custom_optimize_maximize(self, invoker, optimizer):
        result = custom_optimize(f_max_fast, invoker=invoker,
                                 optimizer=optimizer)
        # the function takes integer parameters from 0 to 10 and returns them
        # so we expect its maximum at 10
        eq_(result[0].value, 10)

    def _test_custom_optimize_minimize(self, invoker, optimizer):
        result = custom_optimize(f_min_fast, invoker=invoker,
                                 optimizer=optimizer)
        # the function takes integer parameters from 0 to 10 and returns them
        # so we expect its minimum at 0
        eq_(result[0].value, 0)

    def _test_custom_optimize_maximize_hang_global_timeout(self, invoker,
                                                           optimizer):
        result = custom_optimize(f_max_slow, invoker=invoker, timeout=1,
                                 optimizer=optimizer)
        # the timeout might hide some results
        # so we expect a result between 0 and 10
        assert 0 <= result[0].value <= 10

    def _test_custom_optimize_minimize_hang_global_timeout(self, invoker,
                                                          optimizer):
        result = custom_optimize(f_min_slow, invoker=invoker, timeout=1,
                                 optimizer=optimizer)
        # the timeout might end the execution before we get a result
        # in that case we expect a result of 0, 0 otherwise
        assert result[0].value == 0

    def _test_function_fast(self, function, invoker, optimizer):
        result = custom_optimize(f=function, invoker=invoker,
                            optimizer=optimizer)
        # this should work, but we do not know anything about the result here
        # so just check that there is any result
        assert result is not None

    def _test_function_failing(self, function, invoker, optimizer):
        # it is assumed that there is a best individual
        # so we expect a TypeError when optimizing an always-failing function
        result = custom_optimize(f=function, invoker=invoker,
                            optimizer=optimizer)

        # will not happen
        assert result is None

if __name__ == '__main__':
    nose.runmodule()
