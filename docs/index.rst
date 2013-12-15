.. OrgES documentation master file, created by
   sphinx-quickstart on Tue Oct 15 05:32:18 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TODO: Define "optimal"
TODO: Computation vs Invocation vs Call
TODO: Parameters vs Arguments

OrgES
=====

**OrgES** is a library that assists in finding optimal arguments for black-box
functions in a limited amount of time utilizing multiple processors. OrgES
provides a range of optimization algorithms for different optimization problems.
OrgES is designed for (but not limited to) black-box objective functions with a
few parameters that possibly take a long time to compute. OrgES also provides a
framework for writing your own parallel optimization algorithms (simply called
optimizer).

Quick Overview
--------------

The example below shows how OrgES can be used to find optimal arguments for a
(rather simple) objective function ``f``. OrgES has no information about the
function ``f`` other than it has two float parameters ``a`` and ``b`` (taking
values between -1 and 1) and returns *some* value.

.. code-block:: python

    from orges import param
    from orges.main import optimize

    @param.float("a", interval=[-1, 1], step=0.2)
    @param.float("b", interval=[-1, 1], step=0.5)
    def f(a, b):
        return a**2 + b**2

    args = optimize(f)

.. OrgES will compute the result of `f` for different values of ``a`` and ``b`` in
.. parallel using all available processors.

By default, OrgES uses the :class:`orges.optimizer.saes.SAESOptimizer` as
optimizer. Other optimizers can be used by passing them to the ``optimize``
function as shown with  :class:`orges.optimizer.gridsearch.GridSearchOptimizer`
in the next example.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, optimizer=GridSearchOptimizer())

To limit the time an optimizer has to optimize `f` (called the global timeout)
we can pass a timeout in seconds.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, timeout=60, optimizer=GridSearchOptimizer())

To also limit the time of an individual computation of `f` (called the local
timeout) we can pass a timeout in seconds by using the
:class:`orges.plugins.timeout.TimeoutPlugin`.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer
    from orges.plugins.timeout import TimeoutPlugin

    args = optimize(f, timeout=60, optimizer=GridSearchOptimizer(), plugins=[TimeoutPlugin(2)])

Getting Started
---------------

Installation
^^^^^^^^^^^^

- How to install it

Objective functions
^^^^^^^^^^^^^^^^^^^

Before you can use OrgES to optimize your objective function you need to
actually define it, including a specification of its parameters. An objective
function in OrgES is just a regular python function that is augmented with a
number of available [decorators] that describe its parameters


.. note::

    In OrgES formal parameters and actual parameters are called *parameters* and
    *arguments*, respectively.

Let's say your objective function takes three parameters ``a``, ``b`` and ``g``,
where ``a`` is an integer between -10 and 10, ``b`` is a float between 0.0 and
1.0 and ``g`` is a boolean. To tell OrgES about this, we need the decorators
:func:`orges.param.int`, :func:`orges.param.float` and :func:`orges.param.bool`
and use them as follows.

.. code-block:: python

    from orges import param

    @param.int("a", interval=[-10, 10])
    @param.float("b", interval=[0, 1])
    @param.bool("g", interval=[0, 1])
    def f(a, b, g):
        return some_expensive_computation(a, b, g)

The decorators have to be specified in the same order as the function parameters
and should have the same name. In other words, the top-most decorator has to
specify the left-most function parameter (preferably using the same name) and so
forth.

The ``some_expensive_computation`` stands for anything from doing I/O to number
crunching. If the computation was successful, it should return a numeric value.
If the computation was *not* successful (e.g. no value can be computed for the
given arguments), it should raise a meaningful exception. You should also make
sure that your objective function can run in parallel by avoiding global state
and similar things.

.. note::

    Currently, OrgES only supports minimization of objective functions. To
    maximize your function you should negate its original return value (e.g
    ``-some_expensive_computation(a, b, g)``).

You can give you parameters more meaningful names using the ``title`` option
supported by all parameter decorators. The title will be used instead of the
name whenever its parameter or argument is shown to you.

.. code-block:: python

    from orges import param

    @param.int("a", interval=[-10, 10], "α")
    @param.float("b", interval=[0, 1], "β")
    @param.bool("g", interval=[0, 1], "γ")
    def f(a, b, g):
        return some_expensive_computation(a, b, g)

For other ways of specifying the parameters of an objective functions, see
:ref:`parameter-specification-label`.

.. _optimization-label:

Optimization
^^^^^^^^^^^^

With an objective function defined we can finally start to optimize it. Given an
objective function `f` the easiest way to optimize it is using the function
:func:`orges.main.optimize`.

.. code-block:: python

    from orges.main import optimize

    args = optimize(f)

The return value of ``optimize`` is a list of arguments (see
:class:`orges.args.Arg`) for which the objective function is optimal.

OrgES runs multiple computations of the objective functions in parallel (via the
:class:`orges.invoker.multiprocess.MultiProcessInvoker`). However, other
invokers can choose different ways to compute objective functions. For more
details, see :ref:`invokers-label`.

By default, OrgES uses :class:`orges.optimizer.saes.SAESOptimizer` for the
optimization. Other optimizers can be selected by passing them to ``optimize``
(see :ref:`optimizers-label`).

.. code-block:: python

    from orges.main import optimize
    from orges.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, optimizer=GridSearchOptimizer())

Generally, to optimize an objective function use a suitable function from below.

.. autofunction:: orges.main.optimize(function, param_spec=None, return_spec=None, timeout=None, plugins=[], optimizer=SAESOptimizer())

.. autofunction:: orges.main.custom_optimize

.. _optimizers-label:

Optimizers
^^^^^^^^^^

Optimizers take an objective function and a specification of the parameters and
try to find the optimal parameters. Optimizers are using invokers to actually
compute the result of objective functions and are therefore by default
parallelized.

OrgES comes a range of built-in optimizers that are suitable for most objective
functions. These are listed below.


.. autoclass:: orges.optimizer.saes.SAESOptimizer

.. autoclass:: orges.optimizer.rechenberg.RechenbergOptimizer

.. autoclass:: orges.optimizer.gridsearch.GridSearchOptimizer

.. autoclass:: orges.optimizer.random.RandomOptimizer

For writing your own optimizers see [How to write an Optimizer].


.. _invokers-label:

Invokers
^^^^^^^^

To find optimal parameters OrgES has to compare the results of objective
function computations for various arguments. While optimizers decide for which
arguments the objective function is computed, invokers choose the way *how* it
is actually computed (or as we call it: invoked). The following invokers are
available in OrgES.

.. autoclass:: orges.invoker.multiprocess.MultiProcessInvoker

.. autoclass:: orges.invoker.pluggable.PluggableInvoker

For writing your own invokers, see [How to write an Invoker] for more


.. _plugins-label:

Plugins
^^^^^^^
- What is a plugin?
- PluggableInvoker
- Available plugins

.. autoclass:: orges.plugins.timeout.TimeoutPlugin

.. autoclass:: orges.plugins.print.PrintPlugin

For writing your own plugins, see [How to write a Plugin].

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

