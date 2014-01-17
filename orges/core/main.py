# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

from threading import Timer

from orges.core.returnspec import ReturnSpec
from orges.invoker.multiprocess import MultiProcessInvoker
from orges.invoker.pluggable import PluggableInvoker
from orges.optimizer.saes import SAESOptimizer
from orges.plugins.print import PrintPlugin
from orges.plugins.timeout import TimeoutPlugin


def custom_optimize(f, invoker, param_spec=None, return_spec=None, timeout=None,
                    optimizer=SAESOptimizer()):
    """
    Optimize the given objective function using the specified invoker.

    :param f: Objective function
    :param invoker: Invoker
    :param timeout: Available time for optimization (in seconds)
    :param optimizer: Optimizer
    """
    try:
        param_spec = param_spec or f.param_spec
    except AttributeError:
        raise NoParamSpecError()

    return_spec = return_spec or ReturnSpec(f)

    optimizer.invoker = invoker

    if timeout is not None:
        Timer(timeout, invoker.stop).start()

    return optimizer.optimize(f, param_spec=param_spec, return_spec=return_spec)

def optimize(f, param_spec=None, return_spec=None, timeout=None,
             plugins=[TimeoutPlugin(1), PrintPlugin()],
             optimizer=SAESOptimizer()):
    """
    Optimize the given objective function.

    :param f: Objective function
    :param timeout: Available time for optimization (in seconds)
    :param plugins: List of plugins
    :param optimizer: Optimizer

    """

    invoker = PluggableInvoker(MultiProcessInvoker(), plugins=plugins)

    return custom_optimize(f, invoker, param_spec, return_spec, timeout,
                           optimizer)


class NoParamSpecError(Exception):
    """The error that occurs when no ParamSpec object is provided"""
    pass
