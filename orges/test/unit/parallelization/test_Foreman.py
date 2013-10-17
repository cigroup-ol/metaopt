#!/bin/python

"""
ProcessQueue - runs workers through queues
"""

from __future__ import division
from __future__ import print_function
import time

from orges.parallelization.management.Foreman import Foreman


if __name__ == '__main__':
    START_TIME = time.time()

    RESULTS = Foreman().run()

    print("Sending a task all process workers via a queue took %s seconds" %\
          ((time.time() - START_TIME)))
