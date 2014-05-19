# -*- coding: utf-8 -*-
"""
Optimizer that issues one single invocation, only.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.optimizer.optimizer import Optimizer
from metaopt.util.stoppable import StoppedError


class SingleInvokeOptimizer(Optimizer):
    """
    Optimizer that issues one single invocation, only.
    """
    def __init__(self):
        super(SingleInvokeOptimizer, self).__init__()
        self._outcome = None

    def optimize(self, invoker, param_spec, return_spec):
        del return_spec  # TODO implement me
        args = ArgsCreator(param_spec).args()

        try:
            invoker.invoke(self, args)
        except StoppedError:
            return None

        invoker.wait()

        return args

    def on_error(self, error, fargs, **kwargs):
        del fargs
        del kwargs
        self._outcome = error

    def on_result(self, result, fargs, **kwargs):
        del fargs
        del kwargs
        self._outcome = result
