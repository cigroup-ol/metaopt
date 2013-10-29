"""Collection of no-self-use methods to build a Foreman from."""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from multiprocessing.queues import Queue
from multiprocessing.process import Process

from orges.invoker.multiprocess_lib.model.Worker import Worker
from orges.invoker.multiprocess_lib.model.Worker import Task
from orges.invoker.multiprocess_lib.model.Worker import Pool


def fill_worker_pool(process_count, get_worker):
    """Returns a tuple consisting of workers and their common result queue."""
    # shared result queue
    queue_results = Queue()
    # list of all workers
    workers = []
    for worker_index in range(0, process_count):
        # queue for this get_worker's tasks
        queue_tasks = Queue()
        # construct a get_worker process with the queues
        worker_process = Process(target=get_worker,
                                 args=(worker_index, queue_tasks,
                                       queue_results))
        worker_process.daemon = True
        worker_process.start()
        workers.append(Worker(worker_index, worker_process, queue_tasks, \
                                queue_results))
    return (Pool(workers, queue_results))


def send_tasks_to_workers(get_tasks, worker_pool):
    """Sends a bunch of tasks to all workers in the given get_worker pool."""
    # Config for the ES
    #TODO Get this from the paramspec of f()

    # fill each get_worker's queue with task messages
    for task in get_tasks():
        send_task_to_workers(task, worker_pool)
    send_task_to_workers(Task("DONE"), worker_pool)


def send_task_to_workers(task, worker_pool):
    """Sends a single task to all workers in the given get_worker pool."""
    for worker in worker_pool.workers:
        send_task_to_worker(task, worker)


def send_task_to_worker(task, worker):
    """Sends a single task to all workers in the given get_worker pool."""
    worker.queue_tasks.put(task)


def listen_to_workers(worker_pool, handle_result, handle_error):
    """Listens to the result queue for all workers and dispatches handling."""
    # handle feedback from the workers
    worker_done_count = 0
    while len(worker_pool.workers) != worker_done_count:
        # get a message from the queue
        result = worker_pool.queue_results.get()

        # handle finished get_worker
        if result.performance == "DONE":
            get_worker = worker_pool.workers[result.id]
            get_worker.process.join()
            worker_pool.workers[result.id] = None    # delete reference
            worker_done_count += 1
            continue

        # handle all other results
        handle_result(result)
