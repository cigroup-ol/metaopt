"""
Invoker that uses multiple cores or CPUs respectively.
"""
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from multiprocessing.process import Process
from Queue import Queue

from orges.invoker.base import BaseInvoker
from orges.invoker.multiprocess_lib.management.LibForeman import \
    listen_to_workers
from orges.invoker.multiprocess_lib.model.Worker import Worker, Pool, Task
from orges.invoker.multiprocess_lib.worker.worker_builder import get_worker_for_function


class MultiProcessInvoker(BaseInvoker):
    """Invoker that manages worker processes that do the actual work."""

    def __init__(self, resources, f):
        """
        resources - number of CPUs to use.
        """
        self._caller = None
        self.worker_count = resources  # we spawn one worker per CPU

        # shared result queue
        self.queue_results = Queue()
        # list of all workers
        workers = []
        for worker_index in range(0, self.worker_count):
            # queue for this get_worker's tasks
            queue_tasks = Queue()
            # construct a get_worker process with the queues
            worker_process = Process(target=get_worker_for_function(f), args=(worker_index, queue_tasks,
                                           self.queue_results))
            worker_process.daemon = True
            worker_process.start()
            workers.append(Worker(worker_index, worker_process, queue_tasks, \
                                    self.queue_results))
        self.worker_pool = Pool(workers, self.queue_results)
        self.next_inactive_worker = 0

        # call superclass
        super(MultiProcessInvoker, self).__init__(self, resources)

    @property
    def caller(self):
        """Gets the caller."""
        return self._caller

    @caller.setter
    def caller(self, value):
        """Sets the caller."""
        self._caller = value

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amout of resources of self."""
        pass

    def invoke(self, f, fargs, **vargs):
        """Calls back to self._caller.on_result() for call(f, fargs)."""
        worker = self.worker_pool.workers[self.next_inactive_worker]
        worker.queue_tasks.put(f, fargs)
        worker.queue_tasks.put(Task(f, "DONE"))
        self.next_inactive_worker += 1 % len(self.worker_pool)

    def wait(self):
        """Blocks till all invoke, on_error or on_result calls are done."""
        on_error = self._caller.on_error
        on_result = self.caller.on_result
        listen_to_workers(self.worker_pool, on_result, on_error)
