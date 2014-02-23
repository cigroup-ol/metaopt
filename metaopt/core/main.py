# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

from threading import Timer

from metaopt.core.returnspec import ReturnSpec
from metaopt.invoker.multiprocess import MultiProcessInvoker
from metaopt.invoker.pluggable import PluggableInvoker
from metaopt.optimizer.saes import SAESOptimizer
from metaopt.util.stoppable import StoppedException


def custom_optimize(f, invoker, param_spec=None, return_spec=None, timeout=None,
                    optimizer=SAESOptimizer()):
    """
    Optimize the given objective function using the specified invoker.

    :param f: Objective function
    :param invoker: Invoker
    :param timeout: Available time for optimization (in seconds)
    :param optimizer: Optimizer
    """

    invoker.f = f

    try:
        invoker.param_spec = param_spec or f.param_spec
    except AttributeError:
        raise NoParamSpecError()

    try:
        invoker.return_spec = return_spec or f.return_spec
    except AttributeError:
        invoker.return_spec = ReturnSpec(f)

    if timeout is not None:
        Timer(timeout, invoker.stop).start()

    result = optimizer.optimize(invoker, param_spec=invoker.param_spec,
        return_spec=invoker.return_spec)

    try:
        invoker.stop()
    except StoppedException:
        pass

    return result


def optimize(f, param_spec=None, return_spec=None, timeout=None, plugins=[],
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
