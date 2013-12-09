# -*- coding: utf-8 -*-

from __future__ import division, print_function, with_statement

import sys

from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand


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
    sources=['orges/test/demo/algorithm/client/hangmodule.c']
)

setup(
    author='Renke Grunwald, Bengt Lüers, Jendrik Poloczek',
    author_email='info@orges.org',
    cmdclass={'test': Tox},
    data_files=[("", ["README.rst", "LICENSE.txt", "requirements.txt"])],
    description='OrgES Package - Organic Computing for Evolution Strategies',
    ext_modules=[HANG_MODULE_EXTENSION],
    install_requires=[],
    license="3-Clause BSD",
    name='orges',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE.txt', 'README.rst', 'requirements.txt']},
    tests_require=["tox", "nose", "mock"],
    url='http://organic-es.tumblr.com/',
    version='0.0.1'
)
