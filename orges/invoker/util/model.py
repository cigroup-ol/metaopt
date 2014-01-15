"""
Models for data exchange between components.
"""
from collections import namedtuple


# data structure for results generated by the workers
Error = namedtuple("Error", ["task_id", "function", "args", "vargs",
                             "kwargs", "worker_id", "value"])

# data structure for results generated by the workers
Result = namedtuple("Result", ["task_id", "function", "args", "vargs",
                               "kwargs", "worker_id", "value"])

# data structure for results generated by the workers
Status = namedtuple("Status", ["task_id", "function", "args", "vargs",
                               "kwargs", "worker_id"])

# data structure for results generated by the workers
Task = namedtuple("Task", ["task_id", "function", "args", "vargs", "kwargs"])
