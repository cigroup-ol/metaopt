# -*- coding: utf-8 -*-
"""
Optimizer that issues one single invocation, only.
"""
from __future__ import division, print_function, with_statement

from orges.core.args import ArgsCreator
from orges.optimizer.base import BaseCaller, BaseOptimizer
from orges.util.stoppable import StoppedException


class SingleInvokeOptimizer(BaseOptimizer, BaseCaller):
    """
    Optimizer that issues one single invocation, only.
    """
    def __init__(self):
        self._result = None
        super(SingleInvokeOptimizer, self).__init__()

    def optimize(self, invoker, param_spec, return_spec):
        del return_spec  # TODO implement me
        args = ArgsCreator(param_spec).args()

        try:
            invoker.invoke(self, args)
        except StoppedException:
            return None

        invoker.wait()
        return self._result

    def on_error(self, error, fargs, **kwargs):
        # TODO implement me
        pass

    def on_result(self, result, fargs, **kwargs):
        self._result = result
