# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from threading import Timer

from orges.invoker.multiprocess import MultiProcessInvoker
from orges.invoker.pluggable import PluggableInvoker
from orges.invoker.pluggable import TimeoutInvocationPlugin
from orges.invoker.pluggable import PrintInvocationPlugin
from orges.optimizer.saesoptimizer import SAESOptimizer


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
    invoker = PluggableInvoker(None, MultiProcessInvoker(), plugins=plugins)

    if optimizer is None:
        optimizer = SAESOptimizer()

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
