"""

"""
from __future__ import division, print_function, with_statement

import threading


class _Singleton(type):
    """Thread-safe singleton."""

    _instances = {}
    _instances_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):  # @NoSelf
        try:
            return cls._instances[cls]
        except KeyError:
            with cls._instances_lock:
                cls._instances[cls] = super(_Singleton, cls).__call__(*args,
                                                                      **kwargs)
            return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass
