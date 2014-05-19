# -*- coding: utf-8 -*-
"""MetaOpt

Usage:
  metaopt (-h | --help)
  metaopt --version

Options:
  -h --help        Show this screen.
  -v --version     Show version.

"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
import sys

# First Party
import metaopt


if __name__ == '__main__':

    commands_version = ['-v', '--version']
    commands_help = ['-h', '--help']

    version = " ".join([metaopt.__name__, metaopt.__version__])

    try:
        command = sys.argv[1]
        if command in commands_version:
            print(version)
        else:
            print(__doc__)
    except:
        print(__doc__)
