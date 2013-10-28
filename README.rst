OrgES – Organic Computing for Evolution Strategies
==================================================

Branch `master`

.. image:: https://travis-ci.org/cigroup-ol/orges.png?branch=master
  :target: https://travis-ci.org/cigroup-ol/orges

Branch `develop`

.. image:: https://travis-ci.org/cigroup-ol/orges.png?branch=develop
  :target: https://travis-ci.org/cigroup-ol/orges

OrgES is a Python-based organic computing framework for difficult blackbox optimization problems. It allows easy self-configuration of complex optimization heuristics.

Run OrgES
---------

    $ PYTHONPATH=`pwd` python orges/main.py

Run PyLint
----------

    $ pylint orges

Run pep8
--------

    $ pep8 orges

Run Tests
---------

We need Tox >= 1.6, so if you run into this:

    $ tox
    ERROR: tox version is 1.4.2, required is at least 1.6

Upgrade tox:

    $ [sudo] pip install --upgrade tox

Actually run:

    $ tox

or

    $ python setup.py test

Build Docs
----------

    $ make --directory docs clean
    $ sphinx-apidoc -o docs orges
    $ make --directory docs html
    $ xdg-open docs/_build/html/index.html
