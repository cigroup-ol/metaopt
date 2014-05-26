# -*- coding: utf-8 -*-
"""
Package of integer functions for testing purposes.
"""

from metaopt.objective.integer.failing import FUNCTIONS_FAILING
from metaopt.objective.integer.fast import FUNCTIONS_FAST
from metaopt.objective.integer.slow import FUNCTIONS_SLOW

FUNCTIONS_INTEGER = FUNCTIONS_FAILING + FUNCTIONS_FAST + FUNCTIONS_SLOW
