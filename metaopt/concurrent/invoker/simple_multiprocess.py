# -*- coding: utf-8 -*-
"""
Invoker that invokes objective functions sequentially.
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from multiprocessing import Process, Queue
from uuid import uuid4

# First Party
from metaopt.concurrent.invoker.invoker import Invoker
from metaopt.core.call.call import call
from metaopt.core.stoppable.stoppable import stoppable


class SimpleMultiprocessInvoker(Invoker):
    """Invoker that invokes objective functions sequentially."""

    def __init__(self):
        super(SimpleMultiprocessInvoker, self).__init__()

        self.result_queue = Queue()

        self.workers = []
        self.workers_data = {}

        self.running_worker_count = 0
        self.maximum_worker_count = 5

    @stoppable
    def invoke(self, caller, fargs, **kwargs):
        self._caller = caller
        del caller

        if self.running_worker_count == self.maximum_worker_count:
            result = self.result_queue.get()

            if result:
                self.running_worker_count -= 1
                self.call_on_result(result)
            else:
                for worker in self.workers:
                    worker.terminate()

                return

        self.start_worker(self._caller, fargs, kwargs)

    def start_worker(self, caller, fargs, kwargs):
        worker_name = uuid4()
        worker_data = (caller, fargs, kwargs)

        worker = Process(target=self.worker_target,
                         args=(worker_name, self.result_queue, fargs))

        self.running_worker_count += 1

        self.workers.append(worker)
        self.workers_data[worker_name] = worker_data

        worker.start()

    def worker_target(self, worker_name, result_queue, fargs):
        try:
            actual_result = call(self.f, fargs, self.param_spec, self.return_spec)
        except Exception as exception:
            # The objective function has risen an exception.
            # So the exception becomes the result.
            actual_result = exception

        result = WorkerResult()
        result.worker_name = worker_name
        result.actual_result = actual_result

        result_queue.put(result)

    def wait(self):
        while self.running_worker_count > 0:
            result = self.result_queue.get()

            if result:
                self.running_worker_count -= 1
                self.call_on_result(result)
            else:
                self.result_queue.close()

                for worker in self.workers:
                    worker.terminate()

                break

    def call_on_result(self, result):
        caller, worker_fargs, worker_kwargs = \
            self.workers_data[result.worker_name]

        actual_result = result.actual_result
        caller.on_result(actual_result, worker_fargs, **worker_kwargs)

    def stop(self, reason=None):
        del reason  # TODO
        self.result_queue.put(None)


class WorkerResult(object):
    def __init__(self):
        self._worker_name = None
        self._actual_result = None

    @property
    def worker_name(self):
        return self._worker_name

    @worker_name.setter
    def worker_name(self, value):
        self._worker_name = value

    @property
    def actual_result(self):
        return self._actual_result

    @actual_result.setter
    def actual_result(self, value):
        self._actual_result = value
