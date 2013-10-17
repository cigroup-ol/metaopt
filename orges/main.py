from __future__ import division
from __future__ import print_function

from orges.demo.algorithms.saes import f as saes
from orges.paramspec import ParamSpec
from orges.args import ArgsCreator, call


#TODO take boolean minimize into account
def _optimize(f, param_spec=None, return_spec=None, minimize=True):
    """Generic optimizer function."""
    if param_spec is None:
        param_spec = ParamSpec(f)

    for args in ArgsCreator(param_spec).product():
        print(call(f, args), args)


def minimize(f, param_spec=None, return_spec=None):
    """Optimizes f to return a minimal value."""
    _optimize(f, param_spec=param_spec, return_spec=return_spec, minimize=True)


def maximize(f, param_spec=None, return_spec=None):
    """Optimizes f to return a maximal value."""
    _optimize(f, param_spec=param_spec, return_spec=return_spec, minimize=False)


def main():
    def f(args):
        args["d"] = 2
        args["epsilon"] = 0.0001
        return saes(args)

    param_spec = ParamSpec()

    # Tip
    # 1 (mu=20, lambd=23, tau0=0.5, tau1=0.7)

    param_spec.int("mu").interval((10, 20))
    param_spec.int("lambd").interval((10, 50))
    param_spec.float("tau0").interval((0, 1)).step(0.1)
    param_spec.float("tau1").interval((0, 1)).step(0.1)
    minimize(f, param_spec)

if __name__ == '__main__':
    main()
