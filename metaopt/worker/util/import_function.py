"""
Utility that imports a function.
"""
from __future__ import division, print_function, with_statement


def import_function(function):
    """Imports function given by qualified package name"""
    function = __import__(function, globals(), locals(), ['function'], 0).f
    # function = getattr(__import__(function["module"], globals(), locals(), ['function'], 0), function["name"]) TODO

    # Note that the following is equivalent:
    #     from MyPackage.MyModule import f as function
    # Also note this always imports the function "f" as "function".
    return function
