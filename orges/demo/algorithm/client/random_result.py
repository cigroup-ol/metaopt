"""Worker with a random result."""

from orges.framework.parallelization.model.Worker import Result
import random


def get_worker(index, queue_tasks, queue_results):
    """
    Returns a Result object with a random performance for each task.
    """
    while True:
        queue_tasks.get()

        performance = random.randrange(0, 100)
        result = Result([index, performance])
        queue_results.put(result)
