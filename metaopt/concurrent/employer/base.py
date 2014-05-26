# -*- coding: utf-8 -*-
"""
Abstract invoker defining the API of employer implementations.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import abc


class BaseEmployer(object):
    """
    Abstract invoker defining the API of employer implementations.

    Employers manage a number of workers. Where manage means they employ new
    workers, lay off existing workers or even abandon the whole enterprise.
    Additionally, employers keep track of how many workers they have.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        super(BaseEmployer, self).__init__()

    @abc.abstractmethod
    def employ(self,  number_of_workers=1):
        """
        Employs a new worker.

        :param  number_of_workers: number of workers to employ, defaults to 1.

        :rtype: None
        """
        del number_of_workers
        raise NotImplementedError()

    @abc.abstractmethod
    def lay_off(self, call_id, reason=None):
        """
        Lays off the worker that executes the call given by id, if any.

        :param call_id: ID of the call whose worker shall be stopped.
        :param reason: The reason why this worker was laid off. (optional)

        :rtype: None
        """
        del call_id
        del reason
        raise NotImplementedError()

    @abc.abstractmethod
    def abandon(self, reason=None):
        """
        Lays off all currently employed workers for the given reason.

        :param reason: The reason why the workers were laid off. (optional)

        :rtype: None
        """
        del reason
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def worker_count(self):
        """
        Property for the worker count attribute.

        :rtype: Count of currently employed workers.
        """
        raise NotImplementedError()
