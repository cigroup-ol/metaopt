#!/bin/python

"""
ProcessQueue - runs workers through queues
"""

from __future__ import division
from __future__ import print_function
import time

from orges.parallelization.management.Foreman import Foreman
from orges.demo.worker.payload_function_hang import worker
from orges.demo.task_generator.hang_dummy import ArgsIterator
from orges.demo.result_handler.hang_print import result_handler


if __name__ == '__main__':
    START_TIME = time.time()

    FOREMAN = Foreman(worker, result_handler, ArgsIterator)
    RESULTS = FOREMAN.run()

    print("Sending a task all process workers via a queue took %s seconds" %\
          ((time.time() - START_TIME)))
