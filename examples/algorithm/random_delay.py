"""
Worker with a randomly deterimined work duration.

"""
from __future__ import division, print_function, with_statement

import random
from time import sleep

from orges.invoker.util.worker_provider import Result


def get_worker(index, queue_tasks, queue_results):
    """Gets a worker function that waits a random time for each task."""
    # set payload weight once per lifetime
    delay = random.choice([1, 2, 5, 10])

    while True:
        msg = queue_tasks.get()
        if (msg == 'DONE'):
            queue_results.put(Result(index, 'DONE'))
            break

        # execute payload
        result = sleep(delay / 1000)

        # report each result back
        queue_results.put(Result(index, result))
