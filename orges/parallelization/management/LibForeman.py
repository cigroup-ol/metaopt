"""Collection of no-self-use methods to build a Foreman from."""

from multiprocessing.queues import Queue
from multiprocessing.process import Process
from orges.parallelization.model.Worker import Worker
from orges.parallelization.model.Worker import Task
from orges.parallelization.model.Worker import Pool


def fill_worker_pool(process_count, worker_f):
    """Returns a tuple consisting of workers and their common result queue."""
    # shared result queue
    queue_results = Queue()
    # list of all workers
    workers = []
    for worker_index in range(0, process_count):
        # queue for this worker's tasks
        queue_tasks = Queue()
        # construct a worker process with the queues
        worker_process = Process(target=worker_f,
                                 args=(worker_index, queue_tasks,
                                       queue_results))
        worker_process.daemon = True
        worker_process.start()
        workers.append(Worker(worker_index, worker_process, queue_tasks, \
                                queue_results))
    return (Pool(workers, queue_results))


def send_tasks(worker_pool, gen_args):
    """Sends a bunch of tasks to all workers in the given worker pool."""
    # Config for the ES
    #TODO Get this from the paramspec of f()

    # fill each worker's queue with task messages
    args = gen_args()
    for worker in worker_pool.workers:
        worker.queue_tasks.put(Task(args))
        worker.queue_tasks.put("DONE")

    worker.process.terminate()


def send_task_to_workers(worker_pool, task):
    """Sends a single task to all workers in the given worker pool."""
    #TODO implement me
    pass


def send_task_to_worker(worker, task):
    """Sends a single task to all workers in the given worker pool."""
    #TODO implement me
    pass


def listen_to_workers(worker_pool, result_handler):
    """Listens to the result queue for all workers and dispatches handling."""
    # handle feedback from the workers
    worker_done_count = 0
    while len(worker_pool.workers) != worker_done_count:
        # get a message from the queue
        result = worker_pool.queue_results.get()

        # handle finished worker
        if result.performance == "DONE":
            worker = worker_pool.workers[result.id]
            worker.process.join()
            worker_pool.workers[result.id] = None    # delete reference
            worker_done_count += 1
            continue

        # handle all other results
        result_handler(result)
