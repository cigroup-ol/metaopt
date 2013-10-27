# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from orges.args import ArgsCreator, call

from orges.invoker.pluggable import PluggableInvoker

from orges.invoker.pluggable import TimeoutInvocationPlugin
from orges.invoker.pluggable import PrintInvocationPlugin

from orges.invoker.simple import SimpleInvoker

# from orges.optimizer.saesoptimizer import SAESOptimizer
from orges.optimizer.gridsearchoptimizer import GridSearchOptimizer

from orges.paramspec import ParamSpec

from orges.test.demo.algorithm.client.saes import f as saes

def optimize(function, param_spec=None, return_spec=None, minimize=True):
    """Optimize the given function"""

    try:
        param_spec = param_spec or function.param_spec
    except AttributeError:
        raise NoParamSpecError()

    plugins = [TimeoutInvocationPlugin(1), PrintInvocationPlugin()]
    invoker = PluggableInvoker(None, SimpleInvoker(None), plugins=plugins)

    # optimizer = SAESOptimizer()
    optimizer = GridSearchOptimizer()
    optimizer.invoker = invoker

    optimizer.optimize(function, param_spec)

class NoParamSpecError(Exception):
    """The error that occurs when no ParamSpec object is provided"""
    pass

def minimize(f, param_spec=None, return_spec=None):
    """Optimizes f to return a minimal value."""
    optimize(f, param_spec=param_spec, return_spec=return_spec, minimize=True)


def maximize(f, param_spec=None, return_spec=None):
    """Optimizes f to return a maximal value."""
    optimize(f, param_spec=param_spec, return_spec=return_spec, minimize=False)


def main():
    def f(args):
        args["d"] = 2
        args["epsilon"] = 0.0001
        return saes(args)

    param_spec = ParamSpec()

    # Tip
    # 1 (mu=20, lambd=23, tau0=0.5, tau1=0.7)

    param_spec.int("mu", interval=(10, 100), display_name="μ")
    param_spec.int("lambd", interval=(10, 100), display_name="λ")
    param_spec.float("tau0", interval=(0, 1), step=0.1, display_name="τ1")
    param_spec.float("tau1", interval=(0, 1), step=0.1, display_name="τ2")

    minimize(f, param_spec)

if __name__ == '__main__':
    main()
