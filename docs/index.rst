.. raw:: html

    <style type="text/css">

    a.image-reference {
        border-bottom: None;
    }

    a.image-reference:hover {
        border-bottom: None;
    }

    .figures {
        float: left;
    }

    .figure {
        float: left;
        margin: 10px;
        margin-bottom: 1px;
        width: auto;
        height: 140px;
        width: 200px;
    }

    .figure img {
        display: inline;
    }

    </style>

.. toctree::
   :maxdepth: 2

OrgES
=====

**OrgES** is a library that optimizes black-box functions using a limited amount
of time and utilizing multiple processors. The main focus of OrgES is the
parameter tuning for machine learning and heuristic optimization.

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

To get started with OrgES, we recommend reading the :doc:`getting_started` page.
For some examples see below or visit the :ref:`examples` page.

.. container:: figures

    .. figure:: ./_images/svm_gridsearch_global_timeout_1_thumb.png
        :target: ./examples/svm_gridsearch_global_timeout.html

    .. figure:: ./_images/svm_saes_global_timeout_1_thumb.png
        :target: ./examples/svm_saes_global_timeout.html

    .. figure:: ./_images/svm_saes_global_timeout_1_thumb.png
        :target: ./examples/svm_saes_global_timeout.html

.. raw:: html

    <div style="clear: both"></div>

