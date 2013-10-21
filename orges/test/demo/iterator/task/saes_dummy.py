"""Returns always the same arguments for the saes."""


def get_argument_batches():
    args = {
        'mu': 15,
        'lambd': 100,
        'd': 2,
        'tau0': 0.5,
        'tau1': 0.6,
        'epsilon': 0.0001
    }
    while True:
        yield args
