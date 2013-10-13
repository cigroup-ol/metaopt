from test.algorithms.saes import f as saes
from paramspec import ParamSpec
from args import ArgsCreator, call

def optimize(f, param_spec=None, return_spec=None):
  """Assume f has to be minimized for now."""
  if param_spec is None:
    param_spec = ParamSpec(f)

  args_creator = ArgsCreator(param_spec)

  for args in args_creator.product():
    print call(f, args), args


if __name__ == '__main__':
  def f(args):
    args["d"] = 2
    args["epsilon"] = 0.0001
    return saes(args)

  param_spec = ParamSpec()

  param_spec.int("mu").interval((10, 20))
  param_spec.int("lambd").interval((10, 50))
  param_spec.float("tau0").interval((0, 1)).step(0.1)
  param_spec.float("tau1").interval((0, 1)).step(0.1)

  optimize(f, param_spec)