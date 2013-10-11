#!/bin/python
from __future__ import division
from multiprocessing import Process, Queue, cpu_count
from Queue import Empty
import time
import random

from test.algorithms.saes import f

# Configuration

try:
    PROCESS_COUNT = cpu_count()  # number of parallel processes
except NotImplementedError:
    PROCESS_COUNT = 2  # dual cores are very common, now
MSG_COUNT = 3  # number of task messages per Queue


def worker_delay(queue_tasks, queue_results):
    """
    Dummy worker that does not have any dependencies.
    
    Waits a random time for each message it gets from the queue.
    """
    # set payload weight once per lifetime
    delay = random.choice([1, 2, 5, 10])
    
    while True:
        msg = queue_tasks.get()
        if (msg == 'DONE'):
            queue_results.put('DONE')
            break
        queue_results.put('BUSY')
    
        # payload execution
        time.sleep(delay / 1000)
        

def worker_f(queue_tasks, queue_results):
    """Runs the imported f() with the last queue message as argument."""
    while True:
        args = queue_tasks.get()
        if (args == 'DONE'):
            queue_results.put('DONE')
            break
        queue_results.put('BUSY')
    
        # payload
        f(args)


class Worker():
    """Datastructure for a worker process and attached queues."""
    def __init__(self, process, queue_tasks, queue_results):
        self.process = process
        self.queue_tasks = queue_tasks
        self.queue_results = queue_results


def get_worker():
    """Connects a worker to two queues and returns a worker object."""
    # construct a queue for each direction
    queue_tasks = Queue()
    queue_results = Queue()

    # construct a worker process with the queues
    worker_process = Process(target=worker_f,
                       args=(queue_tasks, queue_results))
    worker_process.daemon = True
    worker_process.start()

    return Worker(worker_process, queue_tasks, queue_results)


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
    for (index, worker) in worker_pool:
        _msg_count = MSG_COUNT
        for i in range(_msg_count):
            worker.queue_tasks.put(args)
        worker.queue_tasks.put("DONE")


def poll_workers(worker_pool):
    """Polls all workers for results, till they are finished."""
    # handle feedback from the workers
    while len(worker_pool):
        for (list_index, (worker_index, (worker)))  in enumerate(worker_pool):
            # get one message, or move on to the next worker
            try:
                msg = worker.queue_results.get_nowait()  # do not wait for a message
            except Empty:
                continue
                
            # handle finished workers
            if msg == "DONE":
                worker.process.join()
                print "Worker %i finished after %f seconds." % (worker_index, time.time() - _start)
                worker_pool.pop(list_index)
                break


if __name__ == '__main__':
    _start = time.time()

    # create pool of workers
    worker_pool = [(i, get_worker()) for i in range(0, PROCESS_COUNT)]

    # send tasks to workers 
    send_tasks(worker_pool)

    # get results
    poll_workers(worker_pool)

    print "Sending %s tasks to %i process workers via a Queue() took %s seconds" % \
          (MSG_COUNT, PROCESS_COUNT, (time.time() - _start))
