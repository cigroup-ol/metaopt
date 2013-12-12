.. OrgES documentation master file, created by
   sphinx-quickstart on Tue Oct 15 05:32:18 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OrgES
=====

**OrgES** is a library that assists in finding optimal parameters for black-box
functions in a limited amount of time utilizing multiple processors. OrgES
provides a range of optimization algorithms for different optimization problems.
OrgES is designed for (but not limited to) black-box objective functions with a
few parameters that possibly take a long time to compute. OrgES also provides a
framework for writing your own parallel optimization algorithms (simply called
optimizer).

Quick Overview
--------------

The example below shows how OrgES can be used to find optimal parameters for a
(rather simple) objective function ``f``. OrgES has no information about the
function ``f`` other than it has two float parameters ``a`` and ``b`` (taking values
between -1 and 1) and returns *some* value.

.. code-block:: python

    from orges import param
    from orges.main import optimize

    @param.float("a", interval=[-1, 1], step=0.1)
    @param.float("b", interval=[-1, 1], step=0.1)
    def f(a, b):
        return a**2 + b**2

    print(optimize(f)) # => (a=0, b=0)

Depending on the number of available processors OrgES will compute the result of
the objective function for different values of ``a`` and ``b`` in parallel.
TODO: More explanations.


By default, OrgES uses the [SAESOptimizer] (a self-adaptive evolutionary
algorithm) as optimizer. Other [optimizers] (such as the [GridSearchOptimizer])
can be used by passing it to the [``optimize``] function.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer

    print(optimize(f, optimizer=GridSearchOptimizer())) # => (a=0, b=0)

Since each optimizer has a different way of finding good parameters, the time to
actually find them varies. To limit the time an optimizer has to find
parameters, the [``timeout``] option can be used. An optimizer immediately
returns the current best parameters when the available time runs out. In the
example below the [GridSearchOptimizer] returns its current best result after 60
seconds.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer

    print(optimize(f, timeout=60, optimizer=GridSearchOptimizer())) # => (a=-0.1, b=-0.2)

To also limit the time of a single objective function computation, [plugins] can
be used.

Getting Started
---------------

Objective functions
^^^^^^^^^^^^^^^^^^^

Before you can use OrgES to optimize your objective function you need to
actually define it, including a specification of its parameters. An objective
function in OrgES is just a regular python function that is augmented with a
number of available [decorators] that describe its parameters

Let's say your objective function takes three parameters ``a``, ``b`` and ``g``,
where ``a`` is an integer between -10 and 10, ``b`` is a float between 0.0 and
1.0 and ``g`` is a boolean. Do tell OrgES about this we need the decorators
[``int``], [``float``] and [``bool``] and use them as follows.

.. code-block:: python

    from orges import param

    @param.int("a", interval=[-10, 10])
    @param.float("b", interval=[0, 1])
    @param.bool("g", interval=[0, 1])
    def f(a, b, g):
        return some_expensive_computation(a, b, g)

Where ``some_expensive_computation`` can be anything from I/O to number
crunching. If the expensive computation was successful, it should return a
numeric value. If the computation was *not* successful (e.g. no value can be
computed for these parameters), it should raise a meaningful exception. You
should also make sure that your objective function can run in parallel by
avoiding global state and similar things.

.. note::

    Currently, OrgES only supports minimization of objective functions. To
    maximize your function you should negate its original return value (e.g
    ``-some_expensive_computation(a, b, g)``).

TODO: step parameter

You can give you parameters more meaningful names using the ``title`` option
supported by all parameter decorators. The title will be used instead of the
name whenever the parameter is shown to you.

.. code-block:: python

    from orges import param

    @param.int("a", interval=[-10, 10], "α")
    @param.float("b", interval=[0, 1], "β")
    @param.bool("g", interval=[0, 1], "γ")
    def f(a, b, g):
        return some_expensive_computation(a, b, g)

TODO: Other ways to specify parameters (manual param_spec)

Optimizer
^^^^^^^^^

.. Timeouts

Plugins
^^^^^^^

Examples
^^^^^^^^

.. Plugin
.. Available plugins
.. How to write plugins

.. Optimizer
.. Available optimizers
.. How to write optimizers

.. Invoker
.. Available invokers
.. How to write invokers

README
======

.. include:: ../README.rst

License
=======

.. include:: ../LICENSE


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

