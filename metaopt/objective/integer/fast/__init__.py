# -*- coding: utf-8 -*-
"""
Package of working integer functions for testing purposes.
"""
from metaopt.objective.integer.fast.explicit import FUNCTIONS_FAST_EXPLICIT
from metaopt.objective.integer.fast.implicit import FUNCTIONS_FAST_IMPLICIT

FUNCTIONS_FAST = FUNCTIONS_FAST_EXPLICIT + FUNCTIONS_FAST_IMPLICIT
