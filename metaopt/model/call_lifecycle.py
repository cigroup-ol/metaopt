# -*- coding: utf-8 -*-
"""
Models for message exchanges between employers and workers.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from collections import namedtuple


# data structure for tasks given to the workers
Call = namedtuple("Call", ["id", "function", "args", "kwargs"])

# data structure for declaring a task is idle before being executed by a worker
Task = namedtuple("Task", ["call"])

# data structure for declaring the start of an execution by the workers
Start = namedtuple("Start", ["worker_id", "call"])

# data structure for declaring a worker generated a result
Result = namedtuple("Result", ["worker_id", "call", "value"])

# data structure for declaring that a worker generated an error
Error = namedtuple("Error", ["worker_id", "call", "value"])

# data structure for declaring that a worker was terminated
Layoff = namedtuple("Layoff", ["worker_id", "call", "value"])
