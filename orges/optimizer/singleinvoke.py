# -*- coding: utf-8 -*-
"""
Optimizer that issues one single invocation, only.
"""
from orges.optimizer.base import BaseOptimizer
from orges.args import ArgsCreator
from collections import namedtuple

# Data structure for results returned by invoke calls and the arguments of such
InvokeResult = namedtuple("InvokeResult", ["arguments", "fitness"])


class SingleInvokeOptimizer(BaseOptimizer):
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

    def optimize(self, F_PACKAGE, param_spec, return_spec, minimize):
        args = ArgsCreator(param_spec).args()

        self._invoker.invoke(F_PACKAGE, args)
        self._invoker.wait()

        return self._result

    def on_error(self, error, args, vargs):
        #TODO
        pass

    def on_result(self, result, args, vargs):
        self._result = InvokeResult(result=result, arguments=args)
