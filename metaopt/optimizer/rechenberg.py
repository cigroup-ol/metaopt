# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from random import sample

# First Party
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.arg.util.modifier import ArgsModifier
from metaopt.core.stoppable.util.exception import StoppedError
from metaopt.optimizer.optimizer import Optimizer
from metaopt.optimizer.util. \
    default_mutation_stength import default_mutation_stength


try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3


class RechenbergOptimizer(Optimizer):
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
        super(RechenbergOptimizer, self).__init__()

        self._invoker = None

        # TODO: Make sure these value are sane
        self.mu = mu
        self.lamb = lamb
        self.a = a

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
        for _ in xrange(self.lamb):
            mother, father = sample(self.population, 2)

            child = ArgsModifier.combine(mother, father)
            child = ArgsModifier.randomize(child, self.sigmas)

            self.population.append(child)

    def score_population(self):
        self.scored_population = []

        for individual in self.population:
            try:
                self._invoker.invoke(self, individual)
            except StoppedError:
                self.aborted = True
                break

        self._invoker.wait()

    def select_parents(self):
        self.scored_population.sort(key=lambda s: s[1])
        new_scored_population = self.scored_population[0:self.mu]
        self.population = map(lambda s: s[0], new_scored_population)

    def change_mutation_strength(self):
        if self.previous_best_fitness is None:
            return  # We can't estimate success probability yet

        successes = len(filter(lambda scored: scored[1] <
                               self.previous_best_fitness,
                               self.scored_population))

        probablity = successes / self.lamb

        # TODO: What happens if sigmas get too large or small
        if probablity > (1 / 5):
            self.sigmas = map(lambda sigma: sigma / self.a, self.sigmas)
        elif probablity < (1 / 5):
            self.sigmas = map(lambda sigma: sigma * self.a, self.sigmas)

    def on_result(self, value, fargs, **kwargs):
        fitness = value
        individual = fargs
        scored_individual = (individual, fitness)
        self.scored_population.append(scored_individual)

        _, best_fitness = self.best_scored_indivual

        if best_fitness is None or fitness < best_fitness:
            self.best_scored_indivual = scored_individual
            self.best_fitness = fitness

    def on_error(self, value, fargs, **kwargs):
            del value  # TODO
            del fargs  # TODO
            del kwargs  # TODO
