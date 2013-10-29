"""
Builds workers for given f()s.
"""
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from orges.invoker.multiprocess_lib.model.Worker import Result


def get_worker_for_function(algorithm_function):
    """Runs the given f() with the last queue message as argument."""
    def worker(index, queue_tasks, queue_results):
        """Worker carrying the f() get_worker_for_function was called with."""
        while True:
            task = queue_tasks.get()
            if (task.args == 'DONE'):
                queue_results.put(Result(index, 'DONE'))
                break

            # execute payload
            result = algorithm_function(task.args)

            # report each result back
            queue_results.put(Result(index, result))
    return worker
