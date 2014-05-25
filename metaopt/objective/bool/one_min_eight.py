# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import minimize


@minimize("value")
@param.bool("a")
@param.bool("b")
@param.bool("c")
@param.bool("d")
@param.bool("e")
@param.bool("f")
@param.bool("g")
@param.bool("h")
def f(**kwargs):
    return sum(kwargs.values())
