"""
TODO document me
"""

from orges.optimizer.gridsearchoptimizer import GridSearchOptimizer
from orges.invoker.singleprocess import SingleProcessInvoker
from orges.invoker.multiprocess import MultiProcessInvoker
from orges.test.demo.algorithm.client.saes import f
from orges.args import ParamSpec


if __name__ == "__main__":
    GSO = GridSearchOptimizer(MultiProcessInvoker(2))
    GSO.optimize(f=f, param_spec=ParamSpec(f=f), return_spec=None,\
                 minimize=True)
    del GSO

    GSO = GridSearchOptimizer(SingleProcessInvoker(2))
    GSO.optimize(f=f, param_spec=ParamSpec(f=f), return_spec=None,\
                 minimize=True)
    del GSO
