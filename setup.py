# -*- coding: utf-8 -*-

from __future__ import division, print_function, with_statement

import sys
from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand

import orges


class Tox(TestCommand):
    """Enables `python setup.py test` to run tox."""
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        try:
            tox.cmdline(self.test_args)
        except SystemExit as exception:
            sys.exit(exception.code)

HANG_MODULE_EXTENSION = Extension(
    'orges.test.unit.hang',
    sources=['orges/examples/algorithm/client/hangmodule.c']
)

setup(
    author=orges.__author__,
    author_email=orges.__author_email__,
    cmdclass={'test': Tox},
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
    data_files=[("", ["README.rst", "LICENSE.txt", "requirements.txt"])],
    description='OrgES Package - Organic Computing for Evolution Strategies',
    ext_modules=[HANG_MODULE_EXTENSION],
    install_requires=[],
    license=orges.__license__,
    name='orges',
    packages=find_packages(exclude=('examples', 'docs', 'tests')),
    package_data={'': ['LICENSE.txt', 'README.rst', 'requirements.txt']},
    setup_requires=["flake8"],
    tests_require=["tox", "nose", "mock"],
    url=orges.__url__,
    version=orges.__version__
)
