#!/bin/python

"""
Tests the foreman object.
"""

from __future__ import division
from __future__ import print_function
import time

from orges.framework.parallelization.management.Foreman import Foreman
from orges.demo.algorithm.client.hang import get_worker
from orges.demo.iterator.task.hang_constant import get_tasks
from orges.demo.handler.result.hang_print import handle_result
from orges.demo.handler.error.hang_retry import handle_error


if __name__ == '__main__':
    START_TIME = time.time()

    FOREMAN = Foreman(get_worker, handle_result, handle_error, get_tasks)
    RESULTS = FOREMAN.run()

    print("Sending a task all process workers via a queue took %s seconds" %\
          ((time.time() - START_TIME)))
