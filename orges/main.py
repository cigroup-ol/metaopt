# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from threading import Timer

from orges.invoker.pluggable import PluggableInvoker
from orges.invoker.pluggable import TimeoutInvocationPlugin
from orges.invoker.pluggable import PrintInvocationPlugin
from orges.invoker.simple import SimpleInvoker
# from orges.optimizer.saesoptimizer import SAESOptimizer
from orges.optimizer.gridsearchoptimizer import GridSearchOptimizer
from orges.paramspec import ParamSpec
from orges.test.demo.algorithm.client.saes import f as saes


def custom_optimize(f, param_spec=None, return_spec=None, timeout=None,
                    optimizer=None, invoker=None):
    """Optimize the given function using the specified optimizer and invoker"""
    try:
        param_spec = param_spec or f.param_spec
    except AttributeError:
        raise NoParamSpecError()

    optimizer.invoker = invoker

    if timeout is not None:
        Timer(timeout, invoker.abort).start()

    return optimizer.optimize(f, param_spec)

def optimize(f, param_spec=None, return_spec=None, timeout=None, plugins=None,
             optimizer=None):
    """Optimize the given function"""

    plugins = [TimeoutInvocationPlugin(1), PrintInvocationPlugin()]
    invoker = PluggableInvoker(None, SimpleInvoker(None), plugins=plugins)

    if optimizer is None:
        optimizer = GridSearchOptimizer()

    return custom_optimize(f, param_spec, return_spec, timeout, optimizer,
                           invoker)


class NoParamSpecError(Exception):
    """The error that occurs when no ParamSpec object is provided"""
    pass


def minimize(f, param_spec=None, return_spec=None):
    """Minimize the given function"""
    optimize(f, param_spec=param_spec, return_spec=return_spec)


def maximize(f, param_spec=None, return_spec=None):
    """Maximize the given function"""
    optimize(f, param_spec=param_spec, return_spec=return_spec)


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
