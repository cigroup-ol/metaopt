Getting Started
---------------

Quick Overview
^^^^^^^^^^^^^^

The example below shows how MetaOpt can be used to find optimal arguments for a
(rather simple) objective function ``f``. MetaOpt needs no information about the
function ``f`` other than it has two float parameters ``a`` and ``b`` (taking
values between -1 and 1) and returns *some* value.

.. code-block:: python

    from metaopt.core import param
    from metaopt.main import optimize

    @param.float("a", interval=[-1, 1], step=0.2)
    @param.float("b", interval=[-1, 1], step=0.5)
    def f(a, b):
        return a**2 + b**2

    args = optimize(f)

MetaOpt will optimize ``f`` in parellel and finally return a list of arguments
for which ``f`` is minimal.

By default, MetaOpt uses the :class:`metaopt.optimizer.saes.SAESOptimizer` as
optimizer. Other optimizers like the
:class:`metaopt.optimizer.gridsearch.GridSearchOptimizer` may also be used.

.. code-block:: python

    from metaopt.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, optimizer=GridSearchOptimizer())

To limit the time an optimizer has to optimize ``f`` we can pass a timeout in
seconds.

.. code-block:: python

    from metaopt.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, timeout=60, optimizer=GridSearchOptimizer())

MetaOpt will return the optimal arguments it found after 60 seconds.

To also limit the time of an individual computation of ``f`` we can pass a
timeout in seconds by using the :class:`metaopt.plugins.timeout.TimeoutPlugin`.

.. code-block:: python

    from metaopt.optimizer.gridsearch import GridSearchOptimizer
    from metaopt.plugins.timeout import TimeoutPlugin

    args = optimize(f, timeout=60, optimizer=GridSearchOptimizer(),
                    plugins=[TimeoutPlugin(5)])

MetaOpt will abort computations of ``f`` that take longer than 5 seconds and
return the optimal arguments it found after 60 seconds.

This should explain the most basic use cases of MetaOpt. For more details we
also recommend reading the next sections.

Installation
^^^^^^^^^^^^

MetaOpt is `available on PyPI`_ and can be installed via the following command:

.. _available on PyPI: https://pypi.python.org/pypi/metaopt

.. code:: bash

    $ sudo pip install metaopt

.. objective-functions-label:
Objective functions
^^^^^^^^^^^^^^^^^^^

Before MetaOpt can be used, an objective function has to be defined. This
includes a specification of its parameters (and optionally its return values).
An objective function in MetaOpt is just a regular Python function that is
augmented with a number of available that describe its parameters (and return
values).

.. note::

    In MetaOpt formal parameters and actual parameters are called *parameters* and
    *arguments*, respectively.

Let's say a particular objective function takes three parameters ``a``, ``b``
and ``g``, where ``a`` is an integer between -10 and 10, ``b`` is a float
between 0.0 and 1.0 and ``g`` is a boolean. To specify these, the decorators
:func:`metaopt.core.param.int`, :func:`metaopt.core.param.float` and
:func:`metaopt.core.param.bool` have to be used as follows.

.. code-block:: python

    from metaopt.core import param

    @param.int("a", interval=[-10, 10])
    @param.float("b", interval=[0, 1])
    @param.bool("g", interval=[0, 1])
    def f(a, b, g):
        return some_expensive_computation(a, b, g)

The decorators have to be specified in the same order as the function parameters
and should have the same name (the first parameter of the decorator). The
topmost decorator has to specify the leftmost function parameter (preferably
using the same name) and so forth.

The ``some_expensive_computation`` stands for anything from doing I/O to number
crunching. If the computation was successful, it should return a numeric value.
If the computation was *not* successful (e.g. no value can be computed for the
given arguments), it should raise a meaningful exception. You should also make
sure that your objective function can run in parallel by avoiding global state
and similar things.

MetaOpt can both maximize and minimize objective functions. To do this, the
:func:`metaopt.core.retuns.maximize` and :func:`metaopt.core.retuns.minimize`
decorators can be used. For example, to maximize the objective function, we use
the `maximize` decorator as follows.

.. code-block:: python

    from metaopt.core.returns import maximize
    from metaopt.core import param

    @maximize("Fitness") # Also give the return value a descriptive name
    @param.int("a", interval=[-10, 10])
    @param.float("b", interval=[0, 1])
    @param.bool("g", interval=[0, 1])
    def f(a, b, g):
        return some_expensive_computation(a, b, g)

By default, MetaOpt minimizes objective functions and using `minimize` is only
required to give the return value a descriptive name.

To also give parameters more descriptive names, the ``title`` option supported
by all parameter decorators can be used. The title will be displayed instead of
the name whenever its parameter or argument is shown to the user.

.. code-block:: python

    from metaopt.core import param

    @param.int("a", interval=[-10, 10], title="α")
    @param.float("b", interval=[0, 1], title="β")
    @param.bool("g", interval=[0, 1], title="γ")
    def f(a, b, g):
        return some_expensive_computation(a, b, g)

The following parameter decorators are available in MetaOpt. More types may be
added in future versions of MetaOpt.

.. autofunction:: metaopt.core.param.int

.. autofunction:: metaopt.core.param.float

.. autofunction:: metaopt.core.param.bool

For more details about specifying the parameters of an objective function, see
:doc:`parameter_specification`.

.. _optimization-label:

Optimization
^^^^^^^^^^^^

With an objective function defined it can be finally optimized. Given an
objective function ``f``, the easiest way to optimize it is using the function
:func:`metaopt.core.main.optimize`.

.. code-block:: python

    from metaopt.main import optimize

    args = optimize(f)

The result of ``optimize`` is a list of arguments (see
:class:`metaopt.core.args.Arg`) for which the objective function is optimal
(either minimial or maximal).

MetaOpt runs multiple computations of the objective functions in parallel (via the
:class:`metaopt.invoker.multiprocess.MultiProcessInvoker`). However, other
invokers can choose different ways to compute objective functions. For more
details, see :ref:`invokers-label`.

By default, MetaOpt uses :class:`metaopt.optimizer.saes.SAESOptimizer` for the
optimization. Other optimizers can be selected by passing them to ``optimize``
(see :ref:`optimizers-label`).

.. code-block:: python

    from metaopt.main import optimize
    from metaopt.optimizer.gridsearch import GridSearchOptimizer

    args = optimize(f, optimizer=GridSearchOptimizer())

Generally, to optimize an objective function use a suitable function from below.

.. autofunction:: metaopt.core.main.optimize(f, timeout=None, plugins=[], optimizer=SAESOptimizer())

.. autofunction:: metaopt.core.main.custom_optimize(f, invoker, timeout=None, optimizer=SAESOptimizer())

.. _optimizers-label:

Optimizers
^^^^^^^^^^

Optimizers take an objective function and a specification of its parameters and
then try to find the optimal parameters. Optimizers are using invokers to
actually compute the result of objective functions and are therefore by default
parallelized.

MetaOpt comes a range of built-in optimizers that are suitable for most types of
objective functions. These are listed below.


.. autoclass:: metaopt.optimizer.saes.SAESOptimizer

.. autoclass:: metaopt.optimizer.rechenberg.RechenbergOptimizer

.. autoclass:: metaopt.optimizer.gridsearch.GridSearchOptimizer

For writing your own optimizers see [How to write an Optimizer].

.. _invokers-label:

Invokers
^^^^^^^^

To find optimal parameters MetaOpt has to compare the results of objective
function computations for various differing arguments. While optimizers decide
for which arguments the objective function is computed, invokers choose the way
*how* it is actually computed (or as we call it: invoked).

Other invokers can be used by passing them to
:func:`metaopt.core.main.custom_optimize`.

.. code-block:: python

    from metaopt.main import custom_optimize
    from metaopt.invoker.multiprocess import MultiProcessInvoker

    args = custom_optimize(f, invoker=invoker)

The following invokers are available in MetaOpt.

.. autoclass:: metaopt.invoker.multiprocess.MultiProcessInvoker

.. autoclass:: metaopt.invoker.dualthread.DualThreadInvoker

.. autoclass:: metaopt.invoker.pluggable.PluggableInvoker

For writing your own invokers, see [How to write an Invoker] for more

.. _plugins-label:

Plugins
^^^^^^^

Plugins change the way objective functions are invoked. They attach handlers to
various events that occur when an optimizer wants to invoke an objective
functions via the :class:`metaopt.invoker.pluggable.PluggableInvoker`.

Plugins can be used by passing them to :func:`metaopt.core.main.optimize`.

.. code-block:: python

    from metaopt.main import optimize

    from metaopt.plugins.timeout import TimeoutPlugin
    from metaopt.plugins.print import PrintPlugin

    args = optimize(f, plugins=[PrintPlugin(), TimeoutPlugin(2)])

If you use your own custom invoker, :func:`metaopt.main.custom_optimize` can be
used.

.. code-block:: python

    from metaopt.main import custom_optimize
    from metaopt.invoker.pluggable import PluggableInvoker

    from metaopt.plugins.timeout import TimeoutPlugin
    from metaopt.plugins.print import PrintPlugin

    invoker = PluggableInvoker(CustomInvoker(),
                               plugins=[PrintPlugin(), TimeoutPlugin(2)])

    args = custom_optimize(f, invoker=invoker)

The following plugins are available in MetaOpt.

.. autoclass:: metaopt.plugins.timeout.TimeoutPlugin

.. autoclass:: metaopt.plugins.print.PrintPlugin

.. autoclass:: metaopt.plugins.visualize.VisualizeLandscapePlugin
   :members: show_image_plot, show_surface_plot

.. autoclass:: metaopt.plugins.visualize.VisualizeBestFitnessPlugin
   :members: show_fitness_invocations_plot, show_fitness_time_plot

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