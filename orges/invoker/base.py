"""
Abstract invoker defining the API of invoker implementations.
"""

from __future__ import division, print_function, with_statement

import abc
from orges.util.stoppable import Stoppable


class BaseInvoker(Stoppable):
    """
    Abstract invoker managing calls to call(f, fargs).

    Invoker implementations also need to be a Stoppable, where the semantic of
    stopping is as follows:

    The invoker calls :meth:`orges.optimizer.base.BaseCaller.on_error` as soon
    as possible for each past call to :meth:`invoke` and raises
    StoppedException for any additional calls to :meth:`invoke`.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, caller):
        super(BaseInvoker, self).__init__()

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
