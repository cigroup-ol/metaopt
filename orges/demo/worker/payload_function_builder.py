""""""
from orges.parallelization.model.Worker import Result


def get_worker_function(algorithm_function):
    def worker(index, queue_tasks, queue_results):
        """Runs the imported f() with the last queue message as argument."""
        while True:
            args = queue_tasks.get()
            if (args == 'DONE'):
                queue_results.put(Result(index, 'DONE'))
                break

            # execute payload
            result = algorithm_function(args)

            # report each result back
            queue_results.put(Result(index, result))
    return worker
