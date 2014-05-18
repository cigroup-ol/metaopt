# -*- coding: utf-8 -*-
"""
Package of integer functions for testing purposes.
"""

from metaopt.test.util.function.integer.failing import FUNCTIONS_FAILING
from metaopt.test.util.function.integer.fast import FUNCTIONS_FAST
from metaopt.test.util.function.integer.slow import FUNCTIONS_SLOW

FUNCTIONS_INTEGER = FUNCTIONS_FAILING + FUNCTIONS_FAST + FUNCTIONS_SLOW
