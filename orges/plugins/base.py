"""This module provides an abstract base class for invocation plugins"""


from abc import abstractmethod, ABCMeta


class BaseInvocationPlugin(object):
    """
    Abstract base class for invocation plugins.

    Plugin developers can either derive their objects directly from this class
    or from :class:`orges.plugins.dummy.DummyInvocationPlugin` to only override
    methods selectively.

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def before_invoke(self, invocation):
        """
        Gets called when pluggable invoker starts preparing a calls to invoke.
        """
        pass

    @abstractmethod
    def on_invoke(self, invocation):
        """
        Gets called right before pluggable invoker calls invoke on its invoker.
        """
        pass

    @abstractmethod
    def on_result(self, invocation):
        """
        Gets called when pluggable invoker receives a callback to on_result.
        """
        pass

    @abstractmethod
    def on_error(self, invocation):
        """
        Gets called when pluggable invoker receives a callback to on_error.
        """
        pass