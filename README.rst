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

.. code:: bash

    $ PYTHONPATH=`pwd` python orges/main.py

Run PyLint
----------

.. code:: bash

    $ pylint orges

Run flake8
----------

.. code:: bash

    $ flake8
    $ python3 setup.py flake8

Run Tests
---------

We need Tox >= 1.6, so if you run into this:

.. code:: bash

    $ tox
    ERROR: tox version is 1.4.2, required is at least 1.6

Upgrade tox:

.. code:: bash

    $ [sudo] pip install --upgrade tox

Actually run:

.. code:: bash

    $ tox

or

.. code:: bash

    $ python setup.py test

Run Coverage
------------

.. code:: bash

    $ nosetests --with-coverage --cover-package=orges

Build Docs
----------

.. code:: bash

    $ make --directory docs clean
    $ sphinx-apidoc -o docs orges
    $ make --directory docs html
    $ xdg-open docs/_build/html/index.html
