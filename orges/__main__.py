"""OrgES

Usage:
  orges run-example <name>...
  orges (-h | --help)
  orges --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

# TODO Figure out what such a command should actually mean and do

from __future__ import division, print_function, with_statement

from docopt import docopt

import orges

if __name__ == '__main__':
    ARGUMENTS = docopt(__doc__, version=" ".join([orges.__name__,
                                                  orges.__version__]))
    print(ARGUMENTS)
