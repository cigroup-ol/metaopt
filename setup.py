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
    data_files=[("", ["README.rst", "LICENSE.txt", "requirements.txt"])],
    description='OrgES Package - Organic Computing for Evolution Strategies',
    ext_modules=[HANG_MODULE_EXTENSION],
    install_requires=[],
    license=orges.__license__,
    name='orges',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE.txt', 'README.rst', 'requirements.txt']},
    setup_requires=["flake8"],
    tests_require=["tox", "nose", "mock"],
    url=orges.__url__,
    version=orges.__version__
)
