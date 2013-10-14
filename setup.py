# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='orges',
    version='0.0.1',
    description='OrgES Package - Organic Computing for Evolution Strategies',
    long_description=open('README.rst').read(),
    author='Renke Grunwald, Bengt Lüers, Jendrik Poloczek',
    author_email='info@orges.org',
    url='http://organic-es.tumblr.com/',
    #TODO use relative path
    license=open('/home/bengt/Arbeit/CI/OrgES/LICENSE').read(),
    packages=find_packages(exclude=('tests', 'docs'))
)
