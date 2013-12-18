# -*- coding: utf-8 -*-
"""
Optimizer that issues one single invocation, only.
"""
from __future__ import division, print_function, with_statement

from orges.args import ArgsCreator
from orges.optimizer.base import BaseCaller, InvokeResult, BaseOptimizer


class SingleInvokeOptimizer(BaseOptimizer, BaseCaller):
    """
    Optimizer that issues one single invocation, only.
    """
    def __init__(self):
        self._result = None
        super(SingleInvokeOptimizer, self).__init__()

    @property
    def invoker(self):
        return self._invoker

    @invoker.setter
    def invoker(self, invoker):
        invoker.caller = self
        self._invoker = invoker

    def optimize(self, function, param_spec, return_spec):
        del return_spec  # TODO implement me
        args = ArgsCreator(param_spec).args()

        self._invoker.invoke(function, args)
        self._invoker.wait()

        return self._result

    def on_error(self, error, args, vargs):
        #TODO
        pass

    def on_result(self, result, args, vargs):
        self._result = InvokeResult(result=result, arguments=args)
