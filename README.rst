OrgES – Organic Computing for Evolution Strategies
==================================================

OrgES is a Python-based organic computing framework for difficult blackbox optimization problems. It allows easy self-configuration of complex optimization heuristics.

Run OrgES
---------

    $ PYTHONPATH=`pwd` python orges/main.py

Run PyLint
----------

    $ pylint orges --rcfile=orges/pylintrc

Run pep8
--------

    $ pep8 orges

Run tox
-------

    $ tox orges

Run Sphinx
----------

    $ make --directory docs clean
    $ sphinx-apidoc -o docs orges
    $ make --directory docs html
    $ xdg-open docs/_build/html/index.html
