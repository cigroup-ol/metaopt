"""Test for the hangmodule C extension."""

from __future__ import division
from __future__ import print_function

from orges.test.unit.hang import hang

if __name__ == '__main__':
    AMOUNT_OF_SECONDS_TO_HANG = 3
    hang(AMOUNT_OF_SECONDS_TO_HANG)
