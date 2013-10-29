"""Returns always the same arguments for the saes."""
from __future__ import division
from __future__ import print_function
from __future__ import with_statement


def get_argument_batches():
    args = {
        'mu': 15,
        'lambd': 100,
        'd': 2,
        'tau0': 0.5,
        'tau1': 0.6,
        'epsilon': 0.0001
    }
    while True:
        yield args
