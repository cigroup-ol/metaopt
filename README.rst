OrgES – Organic Computing for Evolution Strategies
==================================================

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

Run tox
-------

We need Tox >= 1.6, so probably:

    $ [sudo] pip install --upgrade tox

Actually run:

    $ tox orges

Run Sphinx
----------

    $ make --directory docs clean
    $ sphinx-apidoc -o docs orges
    $ make --directory docs html
    $ xdg-open docs/_build/html/index.html
