# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.util import param
from metaopt.core.returnspec.util.decorator import maximize


@maximize("Sum")
@param.multi(param.bool, ["a", "b", "c", "d", "e", "f", "g", "h"])
def f(**kwargs):
    return sum(kwargs.values())
