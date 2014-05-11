# -*- coding: utf-8 -*-
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

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
from docopt import docopt

# First Party
import metaopt


if __name__ == '__main__':
    ARGUMENTS = docopt(__doc__, version=" ".join([metaopt.__name__,
                                                  metaopt.__version__]))
    print(ARGUMENTS)
