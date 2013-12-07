"""This module provides an abstract base class for invocation plugins"""


from abc import abstractmethod, ABCMeta


class BasePlugin(object):
    """
    Abstract base class for invocation plugins.

    Plugin developers can either derive their objects directly from this class
    or from :class:`orges.plugins.dummy.DummyPlugin` to only override
    methods selectively.

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def before_invoke(self, invocation):
        """
        Called right before the invoker calls the objective function

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`orges.invoker.pluggable.Invocation`
        """
        pass

    @abstractmethod
    def on_invoke(self, invocation):
        """
        Called after the invoker called the objective function

        Since objective functions are usually called asyncronously `invocation`
        will not contain any results yet.

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`orges.invoker.pluggable.Invocation`
        """
        pass

    @abstractmethod
    def on_result(self, invocation):
        """
        Called when the invocation of the objective function was successful

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`orges.invoker.pluggable.Invocation`
        """
        pass

    @abstractmethod
    def on_error(self, invocation):
        """
        Called when the invocation of the objective function was not successful

        Since the invocation was not successful `invocation` will not contain
        any result.

        :param invocation: Information about the current (and past) invocations
        :type invocation: :class:`orges.invoker.pluggable.Invocation`
        """
        pass