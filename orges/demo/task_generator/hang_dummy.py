"""Returns always the same arguments for the hang module c extension."""


def args_generator():
    args = 100
    while True:
        yield args
