from __future__ import division
from __future__ import print_function

from numpy.random import randn
from random import sample

from orges.args import ArgsCreator

class CombinedOptimizer():
    def __init__(self, **optimizer):
        pass

class SAESOptimizer(object):
    MU = 10
    LAMBDA = 10
    TAU0 = 0.5
    TAU1 = 0.5

    def __init__(self, invoker):
        self.invoker = invoker

        self.population = []
        self.scored_population = []
        self.best_scored_indivual = None

        self.generation = 1


    def initalize_population(self):
        # TODO implement me
        pass


    def optimize(self, f, param_spec, return_spec=None, minimize=True):
        self.f = f
        self.param_spec = param_spec

        self.initalize_population()
        self.score_population()

        while not self.exit_condition():
            self.add_offspring()
            self.score_population()
            self.select_parents()

            yield self.best_scored_indivual[0]
            self.generation += 1

        return self.best_scored_indivual[0]

    def exit_condition(self):
        pass

    def initalize_popluation(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(SAESOptimizer.MU):
            args = args_creator.random()
            args_sigma = list(randn(len(args)))

            individual = (args, args_sigma)
            self.population.append(individual)

    def add_offspring(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(SAESOptimizer.LAMBDA):
            mother, father = sample(self.population, 2)

            child_args = args_creator.combine(mother[0], father[0])

            mean = lambda x1,x2: (x1 + x2) / 2
            child_args_sigma = map(mean, mother[1], father[1])

            args_creator.randomize(child_args_sigma)

            # TODO: Mutate sigma

            child = (child_args, child_args_sigma)

            self.population.append(child)


    def score_population(self):
        for individual in self.population:
            args, _ = individual
            self.invoker.call(self.f, args, individual)

        self.invoker.wait()

    def select_parents(self):
        self.scored_population.sort(key=lambda s: s[1])
        new_scored_population = self.scored_population[0:SAESOptimizer.MU]
        self.population = map(lambda s: s[0], new_scored_population)

    def on_result(self, args, result, individual):
        _, fitness = result
        scored_individual = (individual, fitness)
        self.scored_population.append(scored_individual)

        best_individual, best_fitness = self.best_scored_indivual

        if fitness < best_fitness:
            self.best_scored_indivual = scored_individual

    def on_error(self, args, error, individual):
        pass
