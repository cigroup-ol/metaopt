# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Extension

HANG_MODULE_EXTENSION = Extension('orges.test.unit.hang',
  sources = ['orges/test/unit/hangmodule.c'])

setup(
  name='orges',
  version='0.0.1',
  description='OrgES Package - Organic Computing for Evolution Strategies',
  long_description=open('README.rst').read(),
  author='Renke Grunwald, Bengt Lüers, Jendrik Poloczek',
  author_email='info@orges.org',
  url='http://organic-es.tumblr.com/',
  license=open("LICENSE").read(),
  packages=find_packages(exclude=('tests', 'docs')),
  ext_modules = [HANG_MODULE_EXTENSION],
  install_requires=open('requirements.txt').read().splitlines()
)
