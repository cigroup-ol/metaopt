"""
Models for data exchange between processes.
"""
from __future__ import division, print_function, with_statement

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
Release = namedtuple("Release", ["worker_id", "call", "value"])
