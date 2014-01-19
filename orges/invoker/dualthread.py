"""
Invoker that runs tasks in an own thread.
"""
from __future__ import division, print_function, with_statement

import uuid
from threading import Lock, Thread

from orges.core.call import call
from orges.invoker.base import BaseInvoker
from orges.util.stoppable import stopping_method, stoppable_method
from orges.invoker.util.task_handle import TaskHandle


class DualThreadInvoker(BaseInvoker):
    """Invoker that runs tasks in an own thread."""

    def __init__(self):
        super(DualThreadInvoker, self).__init__()
        self.thread = None
        self.task = None
        self.lock = Lock()

        self.current_task = None
        self.cancelled = False
        self.aborted = False

    def get_subinvoker(self, resources):
        """Returns a subinvoker using the given amount of resources of self."""
        del resources
        raise NotImplementedError()

    @stoppable_method
    def invoke(self, caller, fargs, *vargs, **kwargs):
        with self.lock:
            if self.aborted:
                return None, True

        self.wait()

        with self.lock:
            self.task = TaskHandle(invoker=self, task_id=uuid.uuid4())

        self.thread = Thread(target=self.target, args=(self.f, fargs),
                             kwargs=kwargs)
        self.thread.start()

        return self.task

    def target(self, f, fargs, *vargs, **kwargs):
        """Target function/method for a thread to execute."""
        # TODO Make this a WorkerThread, subclassing multiprocess.Thread.
        # (Symmetrically to the WorkerProcess)
        value = call(f, fargs)

        with self.lock:
            cancelled = self.cancelled
            self.cancelled = False

        if not cancelled:

            self._caller.on_result(value, fargs, *vargs, **kwargs)
        else:
            self._caller.on_error(value, fargs, *vargs, **kwargs)

    def wait(self):
        if self.thread is not None:
            self.thread.join()

        with self.lock:
            aborted = self.aborted

        return aborted

    @stoppable_method
    @stopping_method
    def stop(self):
        """Stops this invoker."""
        with self.lock:
            self.aborted = True

        self.stop_task(self.current_task)

    def stop_task(self, task):
        """Stops the given task."""
        with self.lock:
            if self.task is not task:
                return

        with self.lock:
            self.cancelled = True
