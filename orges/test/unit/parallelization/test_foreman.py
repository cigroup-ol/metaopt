#!/bin/python

"""
Tests the foreman object.
"""
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

import time

from orges.invoker.multiprocess_lib.management.Foreman import Foreman
from orges.test.demo.iterator.task.hang_constant import get_tasks
from orges.test.demo.handler.result.hang_print import handle_result
from orges.test.demo.handler.error.hang_retry import handle_error
from orges.test.demo.algorithm.client.hang import get_worker


if __name__ == '__main__':
    START_TIME = time.time()

    FOREMAN = Foreman(get_worker, handle_result, handle_error, get_tasks)
    RESULTS = FOREMAN.run()

    print("Sending a task all process workers via a queue took %s seconds" %\
          ((time.time() - START_TIME)))
