"""
Abstract invoker defining the API of invoker implementations.
"""

from __future__ import division, print_function, with_statement

import abc


class BaseInvoker(object):
    """Abstract invoker managing calls to call(f, fargs)."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, caller):
        pass

    @abc.abstractmethod
    def invoke(self, f, fargs, **kwargs):
        """
        Invoke an objective function with given arguments.

        Implementations of this method are expected to have the following
        behavior:

        It applies the objective function `f` to the arguments `fargs` (usually
        via :func:`orges.args.call`). If `f` can be applied right now (e.g.
        enough resources are available) :func:`invoke` should return
        immediately, otherwise :func:`invoke` should block until `f` can be
        applied.

        After `f` was applied successfully the invoker should call
        :meth:`orges.optimizer.base.BaseCaller.on_result` on the caller passing
        the result of the application, `fargs` and `kwargs`. If the application
        of `f` was not successful the invoker should call
        :meth:`orges.optimizer.base.BaseCaller.on_error` passing an error,
        `fargs` and `kwargs`.

        Calls to both `on_result` and `on_error` and should be synchronized and
        thus the invoker has to wait until these methods return before calling
        them again.

        :param f: Objective function
        :param fargs: Arguments `f` should be applied to
        :param kwargs: Additional data arguments

        TODO: Return value
        """
        pass

    @abc.abstractmethod
    def wait(self):
        """
        Wait until `on_result` or `on_error` were called for each
        :meth:`invoke`

        Implementations of this method are expected to have the following
        behavior:

        It waits until :meth:`orges.optimizer.base.BaseCaller.on_result` or
        :meth:`orges.optimizer.base.BaseCaller.on_error` were called for each
        call to :meth:`invoke`.

        TODO: Return value
        """
        pass

    @abc.abstractmethod
    def abort(self):
        """
        Abort all current and future calls to :meth:`invoke`

        Implementations of this method are expected to have the following
        behavior:

        It immediately (or rather as fast as possible) calls
        :meth:`orges.optimizer.base.BaseCaller.on_error` for each call to
        :meth:`invoke`.
        """
        pass


class TaskHandle(object):
    """A means to cancel a task."""

    def __init__(self, invoker, task_id):
        self._invoker = invoker
        self._task_id = task_id

    def cancel(self):
        """Cancels this task."""
        self._invoker.cancel(self._task_id)
