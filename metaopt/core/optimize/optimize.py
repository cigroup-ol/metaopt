# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from threading import Timer

# First Party
from metaopt.concurrent.invoker.multiprocess import MultiProcessInvoker
from metaopt.concurrent.invoker.pluggable import PluggableInvoker
from metaopt.core.optimize.util.exception import GlobalTimeoutError, \
    NoParamSpecError
from metaopt.core.returnspec.returnspec import ReturnSpec
from metaopt.core.stoppable.util.exception import StoppedError
from metaopt.optimizer.saes import SAESOptimizer


def custom_optimize(f, invoker, param_spec=None, return_spec=None,
                    timeout=None, optimizer=SAESOptimizer()):
    """
    Optimizes the given objective function using the specified invoker.

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

    def stop_optimization():
        error = GlobalTimeoutError(
            "The optimization ran out of time (%s seconds)" % timeout
        )

        try:
            invoker.stop(error)
        except StoppedError:
            # The invoker was already stopped.
            # TODO Who might have stopped the invoker?
            # Nothing to do here.
            pass

    if timeout is not None:
        timer = Timer(timeout, stop_optimization)
        timer.start()

    result = optimizer.optimize(invoker=invoker, param_spec=invoker.param_spec,
                                return_spec=invoker.return_spec)

    try:
        invoker.stop()
    except StoppedError:
        pass

    if timeout is not None:
        timer.cancel()

    if result is None:
        return None

    return tuple(result)


def optimize(f, param_spec=None, return_spec=None, timeout=None, plugins=[],
             optimizer=SAESOptimizer()):
    """
    Optimizes the given objective function.

    :param f: Objective function
    :param timeout: Available time for optimization (in seconds)
    :param plugins: List of plugins
    :param optimizer: Optimizer

    """

    invoker = PluggableInvoker(invoker=MultiProcessInvoker(), plugins=plugins)

    return custom_optimize(f, invoker=invoker, param_spec=param_spec,
                           return_spec=return_spec, timeout=timeout,
                           optimizer=optimizer)
