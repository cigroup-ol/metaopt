# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Extension
import os

hang_module_ext = Extension('orges.test.unit.hang', 
  sources = ['orges/test/unit/hangmodule.c'])

setup(
  name='orges',
  version='0.0.1',
  description='OrgES Package - Organic Computing for Evolution Strategies',
  long_description=open('README.rst').read(),
  author='Renke Grunwald, Bengt Lüers, Jendrik Poloczek',
  author_email='info@orges.org',
  url='http://organic-es.tumblr.com/',
  license=open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "LICENSE")).read(),
  packages=find_packages(exclude=('tests', 'docs')),
  ext_modules = [hang_module_ext],
)
