# -*- coding: utf-8 -*-
"""
Integer functions that work and do not state their optimization direction.
"""

from metaopt.objective.integer.fast.implicit.f import f as f
from metaopt.objective.integer.fast.implicit.g import f as g
from metaopt.objective.integer.fast.implicit.h import f as h
from metaopt.objective.integer.fast.implicit.i import f as i
from metaopt.objective.integer.fast.implicit.j import f as j
from metaopt.objective.integer.fast.implicit.k import f as k

FUNCTIONS_FAST_IMPLICIT = [f, g, h, i, j, k]
