# -*- coding: utf-8 -*-
"""
Utility that detects the package of a given object.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import inspect
import os


def determine_package(some_object):
    """
    Resolves a call by object to a call by package.
    - Determine absolute package name of the given object.
    - When the task gets executed, the worker process will import it.
    """

    # expand the module's path to an absolute import
    filename = inspect.getsourcefile(some_object)
    module_path, module_filename = os.path.split(filename)
    module_name, _ = os.path.splitext(module_filename)
    prefix = []
    for directory in module_path.split(os.sep)[::-1]:
        prefix.append(directory)
        candidate = ".".join(prefix[::-1] + [module_name])

        if candidate.startswith("."):
            candidate = candidate[1:]

        try:
            __import__(name=candidate, globals=globals(), locals=locals(),
                       fromlist=[], level=0)
            some_object = candidate
            return some_object
        except ImportError:
            pass
    raise ImportError("Could not determine the package of the given " +
                      "object. This should not happen.")
