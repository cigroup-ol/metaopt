# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement


from threading import Timer

from orges.invoker.multiprocess import MultiProcessInvoker
from orges.invoker.pluggable import PluggableInvoker
from orges.plugins.timeout import TimeoutInvocationPlugin
from orges.plugins.print import PrintInvocationPlugin
from orges.optimizer.saes import SAESOptimizer


def custom_optimize(function, param_spec=None, return_spec=None, timeout=None,
                    optimizer=None, invoker=None):
    """Optimize the given function using the specified optimizer and invoker"""
    try:
        param_spec = param_spec or function.param_spec
    except AttributeError:
        raise NoParamSpecError()

    optimizer.invoker = invoker

    if timeout is not None:
        Timer(timeout, invoker.abort).start()

    return optimizer.optimize(function, param_spec, None, None)


def optimize(function, param_spec=None, return_spec=None, timeout=None,
             plugins=[TimeoutInvocationPlugin(1), PrintInvocationPlugin()],
             optimizer=SAESOptimizer()):
    """Optimize the given function using the specified optimizer and plugins"""

    invoker = PluggableInvoker(MultiProcessInvoker(), plugins=plugins)

    return custom_optimize(function, param_spec, return_spec, timeout,
                           optimizer, invoker)


class NoParamSpecError(Exception):
    """The error that occurs when no ParamSpec object is provided"""
    pass