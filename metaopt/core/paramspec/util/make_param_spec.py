# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.paramspec.paramspec import ParamSpec


def make_param_spec(func):
    """Create a new param_spec object for ``f`` or retrieves it if it exists"""
    try:
        param_spec = func.param_spec
    except AttributeError:
        func.param_spec = param_spec = ParamSpec(via_decorator=True)
    return param_spec
