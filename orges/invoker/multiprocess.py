"""
Invoker that uses multiple processes.
"""

from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from collections import namedtuple
import logging
import multiprocessing
from multiprocessing import Queue, cpu_count
from multiprocessing import Process
from orges.args import call

from orges.invoker.base import BaseInvoker
import uuid

# TODO use Pool from multiprocess
# TODO ensure tasks can be cancelled that are waiting in the queue


class MultiProcessInvoker(BaseInvoker):
    """Invoker that manages worker processes."""

    def __init__(self, resources=None):
        """
        @param resources - number of CPUs to use.
                           will automatically configure itself, if None
        """

        # spawn one worker process per CPU, or as many as requested
        if resources is None:
            try:
                self.worker_count_max = cpu_count()
            except NotImplementedError:
                self.worker_count_max = 2    # dual cores are very common, now
        else:
            self.worker_count_max = resources

        #self.worker_count_max = 1  # TODO

        self.aborted = False

        # set this using the property
        self._caller = None

        # init logging
        self._logger = multiprocessing.log_to_stderr(logging.INFO)

        # queues common to all worker processes
        self._queue_results = Queue()
        self._queue_status = Queue()
        self._queue_tasks = Queue()

        # init worker processes
        self._worker_processes = None
        self._populate_worker_processes()

        super(MultiProcessInvoker, self).__init__(resources=resources,
                                                  caller=self._caller)

    def _populate_worker_processes(self):
        """
        Fills this class with as many worker processes with as many as allowed.
        """
        self._worker_processes = []
        for worker_id in range(self.worker_count_max):
            self._worker_processes.append(self._get_worker_process(worker_id))

    def _provision_worker(self):
        if len(self._worker_processes) is not self.worker_count_max:
            worker_id = uuid.uuid4()
            self._worker_processes.append(self._get_worker_process(worker_id))

    def _get_worker_process(self, worker_id):
        worker_process = WorkerProcess(worker_id=worker_id,
                             queue_tasks=self._queue_tasks,
                             queue_results=self._queue_results,
                             queue_status=self._queue_status)
        worker_process.daemon = True  # disallow workers to spawn processes
        worker_process.start()
        return worker_process

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

    def invoke(self, f_package, fargs, **vargs):
        """
        Puts a task into this Invoker's task queue for the workers to execute.
        """

        #self._logger.warning("invoke entered")

        self._provision_worker()
        task_id = uuid.uuid4()
        self._queue_tasks.put(Task(task_id=task_id, f_package=f_package, args=fargs, vargs=vargs))
        status = self._queue_status.get()
        if status is None:
            self.aborted = True
            task_handle = None
        else:
            task_handle = TaskHandle(self, status.worker_id, status.task_id)

        #self._logger.warning("invoke left")

        return task_handle, self.aborted

    def abort(self):
        """Terminates all worker processes for immediate shutdown."""

        #self._logger.warning("abort entered")

        # shutdown all workers
        for worker_process in self._worker_processes:
            worker_process.report_status()
            worker_process.terminate()
            worker_process.join()
        self.aborted = True

        value = 0
        return (self.aborted, value)

    def terminate_gracefully(self):
        """Sends sentinel objects to all workers to allow clean shutdown."""

        #self._logger.warning("terminate entered")

        for worker_process in self._worker_processes:
            worker_process.queue_tasks.put(None)

    def _count_busy_workers(self):
        #self._logger.warning("count busy workers entered")

        worker_busy_count = 0
        for worker_process in self._worker_processes:
            if worker_process.busy:
                worker_busy_count += 1
        #self._logger.warning(worker_busy_count)
        return worker_busy_count

    def wait(self):
        """
        Blocks till all invoke, on_error or on_result calls are done. Listens
        to the result queue for all workers and dispatches handling.
        """

        #self.terminate_gracefully()

        #self._logger.warning("wait entered")

        while self._count_busy_workers() >= 1:
            #self._logger.warning(self._count_busy_workers())
            # wait for the next result from the queue
            result = self._queue_results.get()

            # handle finished worker
            if result.value == None:
                worker_process = self._worker_processes[result.worker_id]
                self._remove_worker_process(worker_process)
                break

            # handle all other results
            self._caller.on_result(result.value, result.args, **result.vargs)

    def _remove_worker_process(self, worker_process):
        status = Status(worker_id=worker_process.worker_id, f_package=None,
                        args=None, vargs=None)
        worker_process.queue_status.put(status)
        worker_process.terminate()
        worker_process.join()
        #self._logger.warning(self._worker_processes)
        self._worker_processes.remove(worker_process)
        #self._logger.warning(self._worker_processes)

    def cancel(self, worker_id, task_id):
        """Terminates a worker given by id."""
        #self._logger.warning("cancel entered")
        #self._logger.warning(worker_id)

        for worker_process in self._worker_processes:
            if worker_process.worker_id == worker_id and \
                    worker_process.current_task_id == task_id:
                self._remove_worker_process(worker_process)
                return  # worker id is unique, no need to look any further
        # TODO: handle queue corruption, by swapping them out for new ones?

        #self._logger.warning("cancel left")

    def status(self):
        """Reports the status of the workforce."""
        # TODO implement me
        pass


class TaskHandle(object):
    def __init__(self, invoker, worker_id, task_id):
        self._invoker = invoker
        self._worker_id = worker_id
        self.task_id = task_id

    def cancel(self):
        self._invoker.cancel(self._worker_id, self.task_id)


# Datastructure for results generated by the workers
Task = namedtuple("Task", ["task_id", "f_package", "args", "vargs"])

# Datastructure for results generated by the workers
Status = namedtuple("Status", ["task_id", "f_package", "args", "vargs",
                               "worker_id"])

# Datastructure for results generated by the workers
Result = namedtuple("Result", ["task_id", "f_package", "args", "vargs",
                               "worker_id", "value"])


class WorkerProcess(Process):
    """Calls functions with arguments, both given by a queue."""
    def __init__(self, worker_id, queue_tasks, queue_results, queue_status):
        self._worker_id = worker_id
        self._queue_tasks = queue_tasks
        self._queue_results = queue_results
        self._queue_status = queue_status
        self._busy = False
        self._current_task_id = None
        super(WorkerProcess, self).__init__()

    @property
    def worker_id(self):
        """Property for the worker_id attribute of this class."""
        return self._worker_id

    @property
    def queue_tasks(self):
        """Property for the tasks attribute of this class."""
        return self._queue_tasks

    @property
    def queue_status(self):
        """Property for the results attribute of this class."""
        return self._queue_status

    @property
    def queue_results(self):
        """Property for the results attribute of this class."""
        return self._queue_results

    @property
    def busy(self):
        """Property for the results attribute of this class."""
        return self._busy

    @property
    def current_task_id(self):
        """Property for the results attribute of this class."""
        return self._current_task_id

    def run(self):
        for task in iter(self.queue_tasks.get, None):
            self._busy = True
            self._current_task_id = task.task_id
            # announce start of work
            #multiprocessing.log_to_stderr(logging.WARN).warning("a")
            status = Status(task_id=self._current_task_id,
                             worker_id=self._worker_id,
                            f_package=task.f_package,
                            args=task.args, vargs=task.vargs)
            self._queue_status.put(status)

            # the actual call
            f = __import__(task.f_package, globals(), locals(), ['f'], -1).f
            value = call(f, task.args)

            #multiprocessing.log_to_stderr(logging.WARN).warning("b")

            # report result back
            self._queue_results.put(Result(task_id=self._current_task_id,
                                           worker_id=self._worker_id,
                                           f_package=task.f_package,
                                           args=task.args, value=value,
                                           vargs=task.vargs))
            #multiprocessing.log_to_stderr(logging.WARN).warning("c")
            self._busy = False
        # send sentinel back
        #multiprocessing.log_to_stderr(logging.WARN).warning("d")
        self._queue_results.put(Result(id=self._worker_id, f=None,
                                          args=None, vargs=None, value=None))
        #multiprocessing.log_to_stderr(logging.WARN).warning("e")

