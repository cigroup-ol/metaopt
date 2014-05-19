from metaopt.core.returns.util.wrapper import ReturnValuesWrapper


def wrap_return_values(values, return_spec=None):
    return ReturnValuesWrapper(return_spec, values)
