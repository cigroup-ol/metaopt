"""MetaOpt

Usage:
  metaopt run-example <name>...
  metaopt (-h | --help)
  metaopt --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

# TODO Figure out what such a command should actually mean and do

from __future__ import division, print_function, with_statement

from docopt import docopt

import metaopt

if __name__ == '__main__':
    ARGUMENTS = docopt(__doc__, version=" ".join([metaopt.__name__,
                                                  metaopt.__version__]))
    print(ARGUMENTS)