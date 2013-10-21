"""
Returns always the same arguments for the hang module c extension.
"""

from orges.test.demo.iterator.args.ConstantArgsIterator import ConstantArgumentBatchIterator
from orges.test.demo.iterator.task.TaskIterator import TaskIterator
from orges.test.demo.iterator.args.LimitedArgumentBatchIterator import \
    LimitedArgumentBatchIterator


def get_tasks(time_to_sleep_in_seconds=1, limit=2):
    """Returns an argument iterator that lets hang hang for a given time."""
    return LimitedArgumentBatchIterator(TaskIterator(ConstantArgumentBatchIterator(time_to_sleep_in_seconds)), limit)
