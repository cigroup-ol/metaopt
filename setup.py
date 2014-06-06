# -*- coding: utf-8 -*-
"""setup.py script for MetaOpt."""

from __future__ import division, print_function, with_statement
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
from pip.req import parse_requirements

import metaopt


def extract_package_name(requirement):
    return str(requirement.req).replace('-', '_').split('==')[0]


def find_requirements(req_file='requirements.txt'):
    return [extract_package_name(r) for r in parse_requirements(req_file)]

DESCRIPTION = 'MetaOpt is a library that optimizes black-box functions using ' + \
              'a limited amount of time and utilizing multiple processors. ' + \
              'The main focus of MetaOpt is the parameter tuning for machine ' + \
              'learning and heuristic optimization.'
if os.path.isfile('README.rst'):
    LONG_DESCRIPTION = "\n\n".join([open('README.rst').read(),
                                              open('CHANGELOG.rst').read()])
else:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    author=metaopt.__author__,
    author_email=metaopt.__author_email__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing'
    ],
    data_files=[("", ["README.rst", "LICENSE.rst", "requirements_examples.txt",
                      "requirements_lint.txt", "requirements_test.txt"])],
    description=DESCRIPTION,
    ext_modules=[],
    install_requires=[],
    license=metaopt.__license__,
    long_description=LONG_DESCRIPTION,
    name='metaopt',
    packages=find_packages(exclude=('examples', 'docs', 'tests')),
    package_data={'': ['LICENSE.rst', 'README.rst', 'requirements*.txt']},
    setup_requires=[],
    tests_require=find_requirements('requirements_test.txt'),
    test_suite='metaopt.tests',
    url=metaopt.__url__,
    use_2to3=(sys.version_info >= (3,)),
    version=metaopt.__version__,
)
