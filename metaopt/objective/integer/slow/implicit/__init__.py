# -*- coding: utf-8 -*-
"""Slow integer functions that do not state the optimum direction."""

from metaopt.objective.integer.slow.implicit.f import f as f
from metaopt.objective.integer.slow.implicit.g import f as g

FUNCTIONS_SLOW_IMPLICIT = [f, g]
