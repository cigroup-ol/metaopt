"""
Utilities for optimizers.
"""
from collections import namedtuple

# Data structure for results returned by invoke calls and the arguments of such
InvokeResult = namedtuple("InvokeResult", ["arguments", "fitness"])
