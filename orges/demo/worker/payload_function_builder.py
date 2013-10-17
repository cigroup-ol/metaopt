""""""
from orges.parallelization.model.Worker import Result


def get_worker_function(algorithm_function):
    def worker(index, queue_tasks, queue_results):
        """Runs the imported f() with the last queue message as argument."""
        while True:
            task = queue_tasks.get()
            args = task.args
            if (args == 'DONE'):
                queue_results.put(Result(index, 'DONE'))
                break

            # execute payload
            result = algorithm_function(args)

            # report each result back
            queue_results.put(Result(index, result))
    return worker
