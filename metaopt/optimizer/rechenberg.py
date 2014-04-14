# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

from random import sample

from metaopt.core.args import ArgsCreator
from metaopt.optimizer.base import BaseCaller, BaseOptimizer
from metaopt.optimizer.util import default_mutation_stength
from metaopt.util.stoppable import StoppedException

try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3


class RechenbergOptimizer(BaseOptimizer, BaseCaller):
    """
    Optimization based on an ES using Rechenberg's 1/5th success rule

    This optimizer should be combined with a global timeout, otherwise it will
    run indefinitely.

    """
    # TODO: Find good default values
    MU = 100
    LAMBDA = 100
    A = 0.1

    def __init__(self, mu=MU, lamb=LAMBDA, a=A):
        """
        :param mu: Number of parent arguments
        :param lamb: Number of offspring arguments
        """
        self._invoker = None

        # TODO: Make sure these value are sane
        self.mu = mu
        self.lamb = lamb
        self.a = a

        self.f = None
        self.param_spec = None

        self.population = []
        self.scored_population = []
        self.best_scored_indivual = (None, None)

        self.best_fitness = None
        self.previous_best_fitness = None

        self.generation = 1
        self.aborted = False

    def optimize(self, invoker, param_spec, return_spec=None, minimize=True):
        self._invoker = invoker
        self.param_spec = param_spec

        params = param_spec.params.values()
        self.sigmas = [default_mutation_stength(param) for param in params]

        self.initalize_population()
        self.score_population()

        while not self.exit_condition():
            self.add_offspring()
            self.score_population()

            if self.aborted:
                return self.best_scored_indivual[0]

            self.select_parents()
            self.change_mutation_strength()

            self.previous_best_fitness = self.best_fitness
            self.generation += 1

        return self.best_scored_indivual[0]

    def exit_condition(self):
        pass

    def initalize_population(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(self.mu):
            individual = args_creator.random()
            self.population.append(individual)

    def add_offspring(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(self.lamb):
            mother, father = sample(self.population, 2)

            child = args_creator.combine(mother, father)
            child = args_creator.randomize(child, self.sigmas)

            self.population.append(child)

    def score_population(self):
        self.scored_population = []

        for individual in self.population:
            try:
                self._invoker.invoke(self, individual)
            except StoppedException:
                self.aborted = True
                break

        self._invoker.wait()

    def select_parents(self):
        self.scored_population.sort(key=lambda s: s[1])
        new_scored_population = self.scored_population[0:self.mu]
        self.population = map(lambda s: s[0], new_scored_population)

    def change_mutation_strength(self):
        if self.previous_best_fitness is None:
            return  # We can't estimate success probablity yet

        successes = len(filter(lambda scored: scored[1] <
                               self.previous_best_fitness,
                               self.scored_population))

        probablity = successes / self.lamb

        # TODO: What happens if sigmas get too large or small
        if probablity > (1 / 5):
            self.sigmas = map(lambda sigma: sigma / self.a, self.sigmas)
        elif probablity < (1 / 5):
            self.sigmas = map(lambda sigma: sigma * self.a, self.sigmas)

    def on_result(self, result, fargs, **kwargs):
        fitness = result
        individual = fargs
        scored_individual = (individual, fitness)
        self.scored_population.append(scored_individual)

        best_individual, best_fitness = self.best_scored_indivual

        if best_fitness is None or fitness < best_fitness:
            self.best_scored_indivual = scored_individual
            self.best_fitness = fitness

    def on_error(self, error, fargs, individual):
        pass
