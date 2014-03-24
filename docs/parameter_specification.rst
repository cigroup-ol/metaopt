Parameter Specification
=======================

There are two different ways to specify parameters in MetaOpt. You can either use
decorators or specify an :class:`metaopt.core.paramspec.ParamSpec` object manually.
While decorators are the preferred way of specifying parameters, manually
creating this object can be useful in some situations.

Internally, the information about the parameters of an objective functions in a
``ParamSpec`` object. The decorators mentioned in :ref:`objective-functions`
automatically create such an object and attach it to an objective function (by
storing it the ``param_spec`` attribute).

Defining a ``ParamSpec`` this way, however, means that an objective function can
only have a single specification. In some cases it's useful to have different
specifications. To allow this, it's possible to construct ``ParamSpec`` objects
manually and pass them to :func:`metaopt.core.main.optimize`.

.. code-block:: python

    from metaopt.main import optimize
    from metaopt.paramspec import ParamSpec

    def f(a):
        return do_something(a)

    param_spec = ParamSpec()
    param_spec.float("a", interval=[0, 1])

    args = optimize(f, param_spec=param_spec)

The above would be same as this.

.. code-block:: python

    from metaopt.core import param

    @param.float("a", interval=[0, 1])
    def f(a):
        return do_something(a)

    args = optimize(f)
