.. toctree::
   :maxdepth: 2

OrgES
=====

**OrgES** is a library that optimizes black-box functions using a limited amount
of time and utilizing multiple processors.

.. **OrgES** is a library that assists in finding optimal arguments for black-box
.. functions in a limited amount of time and utilizing multiple processors. OrgES
.. provides a range of optimization algorithms for different kind of problems.

.. OrgES is designed for (but not limited to) black-box objective functions with a
.. few parameters that possibly take a long time to compute. OrgES also provides a
.. framework for writing your own parallel optimization algorithms.

.. code-block:: python

    from orges import param
    from orges.main import optimize

    @param.float("a", interval=[-1, 1])
    @param.float("b", interval=[0, 1])
    def f(a, b):
        return a**2 + b**2

    args = optimize(f, timeout=60)


OrgES has the following notable features:

- Custom optimization algorithms
- Custom invocation strategies
- A hook-based plugin system
- Different levels of timeouts


Getting Started
---------------

Quick Overview
^^^^^^^^^^^^^^

The example below shows how OrgES can be used to find optimal arguments for a
(rather simple) objective function ``f``. OrgES needs no information about the
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

OrgES will optimize ``f`` in parellel and then returns a list of arguments for
which ``f`` is minimal.

By default, OrgES uses the :class:`orges.optimizer.saes.SAESOptimizer` as
optimizer. Other optimizers like
the :class:`orges.optimizer.gridsearch.GridSearchOptimizer` can also be used.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, optimizer=GridSearchOptimizer())

To limit the time an optimizer has to optimize ``f`` we can pass a timeout in
seconds.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, timeout=60, optimizer=GridSearchOptimizer())

OrgES will return the optimal arguments it found after 60 seconds.

To also limit the time of an individual computation of ``f`` we can pass a
timeout in seconds by using the :class:`orges.plugins.timeout.TimeoutPlugin`.

.. code-block:: python

    from orges.optimizer.gridsearch import GridSearchOptimizer
    from orges.plugins.timeout import TimeoutPlugin

    args = optimize(f, timeout=60, optimizer=GridSearchOptimizer(), plugins=[TimeoutPlugin(5)])

OrgES will abort computations of ``f`` that take longer than 5 seconds and
return the optimal arguments it found after 60 seconds.

This should explain the most basic use cases of OrgES. For more details we
recommend reading the next sections.

Installation
^^^^^^^^^^^^

- How to install it

.. objective-functions-label:
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
and should have the same name. The topmost decorator has to specify the leftmost
function parameter (preferably using the same name) and so forth.

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

The following paramter decorators are available in OrgES.

.. autofunction:: orges.param.int

.. autofunction:: orges.param.float

.. autofunction:: orges.param.bool

For more details about specifying the parameters of an objective function, see
:doc:`parameter_specification`.

.. _optimization-label:

Optimization
^^^^^^^^^^^^

With an objective function defined we can finally start to optimize it. Given an
objective function ``f`` the easiest way to optimize it is using the function
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

.. autofunction:: orges.main.optimize(f, timeout=None, plugins=[], optimizer=SAESOptimizer())

.. autofunction:: orges.main.custom_optimize(f, invoker, timeout=None, optimizer=SAESOptimizer())

.. _optimizers-label:

Optimizers
^^^^^^^^^^

Optimizers take an objective function and a specification of its parameters and
then try to find the optimal parameters. Optimizers are using invokers to
actually compute the result of objective functions and are therefore by default
parallelized.

OrgES comes a range of built-in optimizers that are suitable for most types of
objective functions. These are listed below.


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
is actually computed (or as we call it: invoked).

Other invokers can be used by passing them to
:func:`orges.main.custom_optimize`.

.. code-block:: python

    from orges.main import custom_optimize
    from orges.invoker.multiprocess import MultiProcessInvoker

    args = custom_optimize(f, invoker=invoker)

The following invokers are available in OrgES.

.. autoclass:: orges.invoker.multiprocess.MultiProcessInvoker

.. autoclass:: orges.invoker.pluggable.PluggableInvoker

For writing your own invokers, see [How to write an Invoker] for more

.. _plugins-label:

Plugins
^^^^^^^

Plugins change the way objective functions are invoked. They attach handlers to
various events that occur when an optimizer wants to invoke an objective
functions for via the :class:`orges.invoker.pluggable.PluggableInvoker`.

Plugins can be used by passing them to :func:`orges.main.optimize`.

.. code-block:: python

    from orges.main import optimize

    from orges.plugins.timeout import TimeoutPlugin
    from orges.plugins.print import PrintPlugin

    args = optimize(f, plugins=[PrintPlugin(), TimeoutPlugin(2)])

If you use your own custom invoker, :func:`orges.main.custom_optimize` can be
used.

.. code-block:: python

    from orges.main import custom_optimize
    from orges.invoker.pluggable import PluggableInvoker

    from orges.plugins.timeout import TimeoutPlugin
    from orges.plugins.print import PrintPlugin

    invoker = PluggableInvoker(CustomInvoker(), plugins=[PrintPlugin(), TimeoutPlugin(2)])

    args = custom_optimize(f, invoker=invoker)

The following plugins are available in OrgES.

.. autoclass:: orges.plugins.timeout.TimeoutPlugin

.. autoclass:: orges.plugins.print.PrintPlugin

For writing your own plugins, see [How to write a Plugin].


.. Plugin
.. Available plugins
.. How to write plugins

.. Optimizer
.. Available optimizers
.. How to write optimizers

.. Invoker
.. Available invokers
.. How to write invokers

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

