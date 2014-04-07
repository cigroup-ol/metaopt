"""
Database that keeps track of worker task relations.
"""
from __future__ import division, print_function, with_statement

from metaopt.invoker.util.model import Error, Release, Result, Start


class StatusDB(object):
    """Database that keeps track of worker task relations."""

    def __init__(self, queue_status, queue_outcome):
        self._queue_start = queue_status
        self._queue_outcome = queue_outcome

        self._task_status_dict = dict()

    def _handle_error(self, error):
        """Handles an error received from the worker via the result queue."""
        self._task_status_dict[error.task.id] = error

    def _handle_result(self, result):
        """Handles a result received from the worker via the result queue."""

        if not result.task.id in self._task_status_dict.keys():
            raise KeyError("No task to be stopped for ID %s" % result.task.id)

        status = self._task_status_dict[result.task.id]
        if isinstance(status, Result):
            raise ValueError("Got duplicate result for task %s." %
                             result.task.id +
                             "Make sure the task ids are unique.")
        #if self._task_status_dict[result.task.id] == None:
            # we got multiple results for the same task
            # that does not make any sense
        #    raise ValueError("There may be only one result per task." +
        #                     " Make sure the IDs are unique.")
        self._task_status_dict[result.task.id] = result

    def _handle_start(self, start):
        """Handles a start received from the worker via the status queue."""
        assert isinstance(start, Start)

#         try:
#             if self._task_status_dict[start.task.id] == start:
#                 # we got the same start repeatedly
#                 # that does not make any sense
#                 raise ValueError("Tasks may not be issued repeatedly." +
#                              " Make sure the IDs are unique.")
#         except KeyError:
#             # we could not find the task id in the database
#             # that is OK, moving on
#             pass

        self._task_status_dict[start.task.id] = start

    def _handle_release(self, release):
        for (task_id, status) in self._task_status_dict.iteritems():
            if release.worker_id == status.worker_id:
                self._task_status_dict[task_id] = release

    def wait_for_one_outcome(self):
        """
        Blocks till one Error or one Result was gotten from the outcome queue
        and processed.
        """
        outcome = self._queue_outcome.get()

        # handle successful results
        if isinstance(outcome, Result):
            self._handle_result(result=outcome)
            return outcome

        # handle error results
        if isinstance(outcome, Error):
            self._handle_error(error=outcome)
            return outcome

        # handle release results
        if isinstance(outcome, Release):
            self._handle_release(release=outcome)
            return outcome

        raise TypeError("%s objects are not allowed in the result queue" %
                        type(outcome))

    def wait_for_one_start(self):
        """
        Blocks till one start was gotten from the start queue and processed.
        """
        start = self._queue_start.get()

        if not isinstance(start, Start):
            raise TypeError("%s objects are not allowed in the start queue" %
                            type(start))

        if start.task.id in self._task_status_dict.keys():
            raise KeyError("Got duplicate start for task %s" % start.task.id +
                           "Make sure IDs are unique.")

        print(start)
        self._handle_start(start=start)
        self._queue_start.task_done()
        return

    def count_running_tasks(self):
        """Returns the number of tasks currently executed by workers."""
        # alternate formulation
        #while len([f for f in self._task_status_dict.values() if t]) > 0:

        count = 0
        for status in self._task_status_dict.values():
            if isinstance(status, Start):
                count += 1
        return count

    def get_worker_id(self, task_id):
        """
        Returns the worker id for a given task id.

        Raises KeyError if there was no worker for that task id. That means,
        all workers were killed before one could start working on the task.
        """
        status = self._task_status_dict[task_id]
        return status.worker_id

    def get_running_task(self, worker_id):
        #assert False
        #import pdb; pdb.set_trace()
        #while True:
            #print("statuses:", len(statuses)) # TODO
            #raise

        #self.wait_for_one_start()
        task_found = False
        for status in self._task_status_dict.values():
            if not status.worker_id == worker_id:
                continue
            if not isinstance(status, Start):
                continue
            task_found = True
            break

        if not task_found:
            raise KeyError("No status for the worker with id: %s" % worker_id)

#         if len(statuses) == 1:
#             break

        return status.task
