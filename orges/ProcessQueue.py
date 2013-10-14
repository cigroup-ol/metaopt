#!/bin/python

"""
ProcessQueue - runs workers through queues
"""

from __future__ import division
from __future__ import print_function
from multiprocessing import Process, Queue, cpu_count
from collections import namedtuple
import time
import random

from orges.test.algorithms.saes import f

# (Semi Auto) Configuration

try:
  PROCESS_COUNT = cpu_count()  # number of parallel processes
except NotImplementedError:
  PROCESS_COUNT = 2  # dual cores are very common, now


def worker_delay(index, queue_tasks, queue_results):
  """
  Dummy worker that does not have any dependencies.

  Waits a random time for each message it gets from the queue.
  """
  # set payload weight once per lifetime
  delay = random.choice([1, 2, 5, 10])

  while True:
    msg = queue_tasks.get()
    if (msg == 'DONE'):
      queue_results.put(Result(index, 'DONE'))
      break

    # execute payload
    result = time.sleep(delay / 1000)

    # report each result back
    queue_results.put(Result(index, result))


# Datastructure for results generated by the workers
Result = namedtuple("Result", ["id", "performance"])


def worker_f(index, queue_tasks, queue_results):
  """Runs the imported f() with the last queue message as argument."""
  while True:
    args = queue_tasks.get()
    if (args == 'DONE'):
      queue_results.put(Result(index, 'DONE'))
      break

    # execute payload
    result = f(args)

    # report each result back
    queue_results.put(Result(index, result))


# data structure for a worker process and attached queues
Worker = namedtuple("Worker", ["id", "process", "queue_tasks", "queue_results"])

# data struture for a pool of workers
WorkerPool = namedtuple("WorkerPool", ["workers", "queue_results"])

def fill_worker_pool(process_count):
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
                 args=(worker_index, queue_tasks, queue_results))
    worker_process.daemon = True
    worker_process.start()
    workers.append(Worker(worker_index, worker_process, queue_tasks, \
                queue_results))
  return (WorkerPool(workers, queue_results))


def send_tasks(worker_pool):
  """Sends a bunch of tasks to all workers in the given worker pool."""
  # Config for the ES
  #TODO Get this from the paramspec of f()
  args = {
    'mu' : 15,
    'lambd' : 100,
    'd' : 2,
    'tau0' : 0.5,
    'tau1' : 0.6,
    'epsilon' : 0.0001
  }

  # fill each worker's queue with task messages
  for worker in worker_pool.workers:
    worker.queue_tasks.put(args)
    worker.queue_tasks.put("DONE")


def listen_to_workers(worker_pool):
  """Listens to the result queue for all workers and dispatches handling."""
  # handle feedback from the workers
  worker_done_count = 0
  while len(worker_pool.workers) != worker_done_count:
    # get a message from the queue
    result = worker_pool.queue_results.get()

    # handle finished workers
    if result.performance == "DONE":
      worker = worker_pool.workers[result.id]
      worker.process.join()
      print("Worker %i finished after %f seconds." % \
          (result.id, time.time() - _start))
      worker_pool.workers[result.id] = None  # delete reference
      worker_done_count += 1
      continue

    # handle all other results
    handle_result(result)


def handle_result(result):
  """Handles a result"""
  #TODO Actually handle the results
  pass


if __name__ == '__main__':
  _start = time.time()

  # create pool of workers
  worker_pool = fill_worker_pool(PROCESS_COUNT)

  # send tasks to workers
  send_tasks(worker_pool)

  # get results
  listen_to_workers(worker_pool)

  print("Sending a task to %i process workers via a Queue() took %s seconds" % \
      (PROCESS_COUNT, (time.time() - _start)))
