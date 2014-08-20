def create_scored_individuals(invoker, individual_factory, fargs_extractor, n_individuals, other_caller=None):
    scored_individuals = []
    n_missing = n_individuals

    while(n_missing > 0):
        n_missing = n_individuals - len(scored_individuals)

        individuals = [individual_factory()
            for _ in range(n_missing)]

        scored_individuals += score_individuals(invoker, fargs_extractor, individuals, other_caller)

    return scored_individuals

def score_individuals(invoker, fargs_extractor, individuals, other_caller=None):
    if not individuals:
        return []

    score_caller = ScoreIndividualCaller(other_caller)

    for individual in individuals:
        fargs = fargs_extractor(individual)
        invoker.invoke(score_caller, fargs, individual=individual)

    invoker.wait()

    return score_caller.scored_individuals


class ScoreIndividualCaller(object):
    def __init__(self, other_caller=None):
        self.other_caller = other_caller
        self.scored_individuals = []

    def on_result(self, result, fargs, individual, **kwargs):
        if self.other_caller:
            self.other_caller.on_result(result, fargs, individual, **kwargs)

        scored_individual = (individual, result)
        self.scored_individuals.append(scored_individual)

    def on_error(self, error, fargs, individual, **kwargs):
        if self.other_caller:
            self.other_caller.on_error(error, fargs, individual, **kwargs)