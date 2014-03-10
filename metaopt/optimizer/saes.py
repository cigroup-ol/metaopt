# -*- coding: utf-8 -*-
"""
Optimizer implementing a self-adapting evolutionary strategy (SAES).
"""
from __future__ import division, print_function, with_statement

from math import exp
from random import gauss, sample

from metaopt.core.args import ArgsCreator
from metaopt.optimizer.base import BaseCaller, BaseOptimizer
from metaopt.optimizer.util import default_mutation_stength
from metaopt.util.stoppable import StoppedException

try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3

class SAESOptimizer(BaseOptimizer, BaseCaller):
    """
    Optimization based on a self-adaptive evolution strategy (SAES)

    This optimizer should be combined with a global timeout, otherwise it will
    run indefinitely.

    """
    MU = 100
    LAMBDA = 100
    TAU0 = 0.5
    TAU1 = 0.5

    def __init__(self, mu=MU, lamb=LAMBDA, tau0=TAU0, tau1=TAU1):
        """
        :param mu: Number of parent arguments
        :param lamb: Number of offspring arguments
        """
        self._invoker = None

        # TODO: Make sure these value are sane
        self.mu = mu
        self.lamb = lamb
        self.tau0 = tau0
        self.tau1 = tau1

        self.invoker = None
        self.param_spec = None

        self.population = []
        self.scored_population = []
        self.best_scored_indivual = (None, None)

        self.aborted = False
        self.generation = 1

    def optimize(self, invoker, param_spec, return_spec=None, minimize=True):
        self.invoker = invoker
        self.param_spec = param_spec

        self.initalize_population()
        self.score_population()

        while not self.exit_condition():
            self.add_offspring()
            self.score_population()

            if self.aborted:
                return self.best_scored_indivual[0][0]

            self.select_parents()

            self.generation += 1

        return self.best_scored_indivual[0][0]

    def exit_condition(self):
        pass

    def initalize_population(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(self.mu):
            args = args_creator.random()
            args_sigma = [default_mutation_stength(arg.param) for arg in args]

            individual = (args, args_sigma)
            self.population.append(individual)

    def add_offspring(self):
        args_creator = ArgsCreator(self.param_spec)

        for _ in xrange(self.lamb):
            mother, father = sample(self.population, 2)

            child_args = args_creator.combine(mother[0], father[0])

            mean = lambda x1, x2: float((x1 + x2) / 2)
            child_args_sigma = map(mean, mother[1], father[1])

            child_args = args_creator.randomize(child_args, child_args_sigma)

            tau0_random = gauss(0, 1)

            def mutate_sigma(sigma):
                tau0 = self.tau0
                tau1 = self.tau1
                return sigma * exp(tau0 * tau0_random) \
                    * exp(tau1 * gauss(0, 1))

            child_args_sigma = map(mutate_sigma, child_args_sigma)

            child = (child_args, child_args_sigma)

            self.population.append(child)

    def score_population(self):
        self.scored_population = []

        for individual in self.population:
            args, _ = individual

            try:
                self.invoker.invoke(self, args, individual=individual)
            except StoppedException:
                self.aborted = True
                break

        self.invoker.wait()

    def select_parents(self):
        self.scored_population.sort(key=lambda s: s[1])
        new_scored_population = self.scored_population[0:self.mu]
        self.population = map(lambda s: s[0], new_scored_population)

    def on_result(self, result, fargs, individual, **kwargs):
        # _, fitness = result
        fitness = result
        scored_individual = (individual, fitness)
        self.scored_population.append(scored_individual)

        best_individual, best_fitness = self.best_scored_indivual

        if best_fitness is None or fitness < best_fitness:
            self.best_scored_indivual = scored_individual

    def on_error(self, fargs, individual, **kwargs):
        pass
