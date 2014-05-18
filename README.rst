MetaOpt
=======

MetaOpt is a Python-based organic computing framework for difficult blackbox
optimization problems. It allows easy self-configuration of complex
optimization heuristics.

For a user guide, see `the documentation`_.
The following describes basic operations with the repository.

.. _the documentation: http://metaopt.readthedocs.org/

Status
------

======== =============== ============= ======== =========
PyPIn    |download|      |version|     |format| |license|
======== =============== ============= ======== =========

======== =============== ================ ==================
master   |Build Master|  |Health Master|  |Coverage Master|
develop  |Build Develop| |Health Develop| |Coverage Develop|
======== =============== ================ ==================

.. |download| image:: https://pypip.in/download/metaopt/badge.png
        :target: https://pypi.python.org/pypi/metaopt/
        :alt: PyPIn downloads

.. |version| image:: https://pypip.in/version/metaopt/badge.png
        :target: https://pypi.python.org/pypi/metaopt/
        :alt: PyPIn version

.. |format| image:: https://pypip.in/format/metaopt/badge.png
        :target: https://pypi.python.org/pypi/metaopt/
        :alt: PyPIn Download Format

.. |license| image:: https://pypip.in/license/metaopt/badge.png
        :target: https://pypi.python.org/pypi/metaopt/
        :alt: PyPIn License

.. |Build Master| image:: https://travis-ci.org/cigroup-ol/metaopt.png?branch=master
        :target: https://travis-ci.org/cigroup-ol/metaopt
        :alt: Build Status

.. |Health Master| image:: https://landscape.io/github/cigroup-ol/metaopt/master/landscape.png
        :target: https://landscape.io/github/cigroup-ol/metaopt/master
        :alt: Code Health

.. |Build Develop| image:: https://travis-ci.org/cigroup-ol/metaopt.png?branch=develop
        :target: https://travis-ci.org/cigroup-ol/metaopt
        :alt: Build Status

.. |Health Develop| image:: https://landscape.io/github/cigroup-ol/metaopt/develop/landscape.png
        :target: https://landscape.io/github/cigroup-ol/metaopt/develop
        :alt: Code Health

.. |Coverage Develop| image:: https://coveralls.io/repos/cigroup-ol/metaopt/badge.png?branch=develop
  :target: https://coveralls.io/r/cigroup-ol/metaopt?branch=develop

.. |Coverage Master| image:: https://coveralls.io/repos/cigroup-ol/metaopt/badge.png?branch=master
  :target: https://coveralls.io/r/cigroup-ol/metaopt?branch=master


Download
--------

MetaOpt is obtainable via `archives of past releases`_,
but you can also get the sources by cloning the repository.

.. _archives of past releases: https://github.com/cigroup-ol/metaopt/releases

To get a working copy of the MetaOpt repository:

.. code:: bash

    $ git clone https://github.com/cigroup-ol/metaopt.git

Installation
------------

MetaOpt is `available on PyPI`_, but you can also install it from source.

.. _available on PyPI: https://pypi.python.org/pypi/metaopt

To install MetaOpt from PyPI using pip:

.. code:: bash

    $ sudo pip install metaopt

To install MetaOpt from a working copy:

.. code:: bash

    $ cd metaopt
    $ sudo pip install -r requirements.txt
    $ sudo python setup.py install

Tests
-----

MetaOpt has `automated online tests`_, but you can also run them locally.

.. _automated online tests: https://travis-ci.org/cigroup-ol/metaopt

To run MetaOpt's test suite from a working copy:

.. code:: bash

    $ cd metaopt
    $ make tests-all
    
Coverage
--------

MetaOpt has `automated online test coverage reports`_, but you can also create them locally.

.. _automated online test coverage reports: https://coveralls.io/r/cigroup-ol/metaopt

To create MetaOpt's coverage reports from a working copy:

.. code:: bash

    $ cd metaopt
    $ make coverage

Examples
--------

MetaOpt comes with `examples, which you can view in the docs`_, but you can also run them locally.

.. _examples, which you can view in the docs: http://metaopt.readthedocs.org/en/latest/examples/index.html

To install MetaOpt's example dependecies and run an example from a working copy:

.. code:: bash

    $ cd metaopt
    $ sudo pip install -r requirements_examples.txt
    $ PYTHONPATH=. python examples/svm_saes_global_timeout.py

Documentation
-------------

MetaOpt has `automatically generated online documentation`_, but you can build
yourself a local copy.

.. _automatically generated online documentation: http://metaopt.readthedocs.org/

To build MetaOpt's html documentation from a working copy:

.. code:: bash

    $ sudo pip install -r requirements_docs.txt
    $ make docs
