# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.arg.arg import Arg
from metaopt.core.arg.bool import BoolArg
from metaopt.core.arg.int import IntArg


def create_arg(param, value=None):
    """Factory method for creating args from params"""

    if param.type == "bool":
        return BoolArg(param, value)
    elif param.type == "int":
        return IntArg(param, value)
    else:
        return Arg(param, value)
