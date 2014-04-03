"""
Database that keeps track of worker task relations.
"""
from __future__ import division, print_function, with_statement

from metaopt.invoker.util.model import Error, Release, Result, Start


class StatusDB(object):
    """Database that keeps track of worker task relations."""

    def __init__(self, queue_status, queue_outcome):
        self._queue_status = queue_status
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

    def _handle_finish(self, finish):
        """Handles a finish received from the worker via the status queue."""

#         try:
#             if self._task_status_dict[finish.task.id] == None:
#                 # we got the same start repeatedly
#                 # that does not make any sense
#                 raise ValueError("Tasks may not be issued repeatedly." +
#                              " Make sure the IDs are unique.")
#         except KeyError:
#             # we could not find the task id in the database
#             # that is OK, moving on
#             pass

        # remove done task
#         if self._task_status_dict[finish.task.id] == finish.worker_id:
#             # always true
#             self._task_status_dict[finish.task.id] = None
#         else:
#             # wont happen
#             # Another start has occurred in the mean time.
#             # The dictionary entry is already up to date.
#             # Do nothing.
#             pass

        self._task_status_dict[finish.task.id] = finish

    def _handle_release(self, release):
        for (task_id, status) in self._task_status_dict.iteritems():
            if release.worker_id == status.worker_id:
                self._task_status_dict[task_id] = release

    def wait_for_one_outcome(self):
        """
        Blocks till one Error or one Result was gotten from the outcome queue
        and processed.
        """
        while True:
            outcome = self._queue_outcome.get()

            # handle successful results
            if isinstance(outcome, Result):
                self._handle_result(result=outcome)
                return outcome

            # handle error results
            elif isinstance(outcome, Error):
                self._handle_error(error=outcome)
                return outcome

            # handle release results
            elif isinstance(outcome, Release):
                self._handle_release(release=outcome)
                return outcome

            raise TypeError("%s objects are not allowed in the result queue" %
                                type(outcome))

    def wait_for_one_status(self):
        """
        Blocks till one status was gotten from the status queue and processed.
        """
        status = self._queue_status.get()

        if not isinstance(status, Start):
            raise TypeError("%s objects are not allowed in the status queue" %
                            type(status))

        if status.task.id in self._task_status_dict.keys():
            raise KeyError("Got duplicate start for task %s" % status.task.id +
                           "Make sure IDs are unique.")

        print(status)
        self._handle_start(start=status)
        self._queue_status.task_done()
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
        """Returns the worker id for a given task id."""
        status = self._task_status_dict[task_id]
        return status.worker_id

    def get_running_task(self, worker_id):
        statuses = []
        import pdb; pdb.set_trace()
        while len(statuses) != 1:
            #print("statuses:", len(statuses)) # TODO
            #raise

            self.wait_for_one_outcome()

            statuses = []
            for status in self._task_status_dict.values():
                if not status.worker_id == worker_id:
                    continue
                if  isinstance(status, (Result, Error, Release)):
                    continue
                statuses.append(status)

        assert len(statuses) == 1
        assert statuses[0].task is not None
        return statuses[0].task
