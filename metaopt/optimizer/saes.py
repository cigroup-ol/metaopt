# -*- coding: utf-8 -*-
"""
Optimizer implementing a self-adapting evolutionary strategy (SAES).
"""
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from math import exp, sqrt
from random import gauss, sample

# First Party
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.core.arg.util.modifier import ArgsModifier
from metaopt.core.stoppable.util.exception import StoppedError
from metaopt.optimizer.optimizer import Optimizer

from metaopt.optimizer.util.default_mutation_strength\
    import default_mutation_strength

from metaopt.optimizer.util.population import create_scored_individuals


try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3


class SAESOptimizer(Optimizer):
    """
    Optimization based on a self-adaptive evolution strategy (SAES)

    This optimizer should be combined with a global timeout, otherwise it will
    run indefinitely.

    """
    MU = 15
    LAMBDA = 100

    def __init__(self, mu=MU, lamb=LAMBDA, tau0=None, tau1=None):
        """
        :param mu: Number of parent arguments
        :param lamb: Number of offspring arguments
        """
        super(SAESOptimizer, self).__init__()

        self.mu = mu
        self.lamb = lamb

        self.tau0 = tau0
        self.tau1 = tau1

        self.param_spec = None
        self.invoker = None

        self.scored_parents = []
        self.scored_children = []

        self.best_scored_individual = (None, None) # (Individual, Fitness)

        self.generation = 1

    def optimize(self, invoker, param_spec, return_spec=None):
        del return_spec

        self.param_spec = param_spec
        self.invoker = invoker

        self.initialize_tau()

        try:
            self.scored_parents = create_scored_individuals(
                self.invoker, self.create_parent, self.extract_fargs, self.mu, self)

            while not self.exit_condition():
                self.scored_children = create_scored_individuals(
                    self.invoker, self.create_child, self.extract_fargs, self.lamb, self)

                self.scored_parents = self.select_parents(
                    self.scored_parents + self.scored_children)

                self.generation += 1
        except StoppedError:
            pass

        return self.extract_best_fargs()

    def initialize_tau(self):
        """
        For a detailed description of the heuristic used to intialize tau0 and
        tau1 see:

        Schwefel H-P (1995) Evolution and Optimum Seeking. Wiley, New York, NY,
        p. 388
        """

        N = self.param_spec.dimensions

        if self.tau0 is None:
            self.tau0 = 1 / sqrt(2 * N)

        if self.tau1 is None:
            self.tau1 = 1 / sqrt(2 * sqrt(N))

    def extract_fargs(self, indivdual):
        return indivdual[0]

    def extract_best_fargs(self):
        if self.best_scored_individual[0]:
            return self.extract_fargs(self.best_scored_individual[0])
        return None

    def create_child(self):
        scored_mother, scored_father = sample(self.scored_parents, 2)

        mother, _ = scored_mother
        father, _ = scored_father

        child_args = ArgsModifier.combine(mother[0], father[0])

        mean = lambda x1, x2: float((x1 + x2) / 2)
        child_args_sigma = map(mean, mother[1], father[1])

        child_args = ArgsModifier.mutate(child_args, child_args_sigma)

        self.tau0_random = gauss(0, 1)

        def mutate_sigma(sigma):
            tau0_mutated = self.tau0 * self.tau0_random
            tau1_mutated = self.tau1 * gauss(0, 1)
            return sigma * exp(tau0_mutated) * exp(tau1_mutated)

        child_args_sigma = map(mutate_sigma, child_args_sigma)

        child = (child_args, child_args_sigma)

        return child

    def create_parent(self):
        args_creator = ArgsCreator(self.param_spec)

        args = args_creator.random()
        args_sigma = [default_mutation_strength(arg.param) for arg in args]

        individual = (args, args_sigma)
        return individual

    def exit_condition(self):
        pass

    def select_parents(self, scored_individuals):
        sorted_scored_individuals = sorted(
            scored_individuals, key=lambda i: i[1])

        return sorted_scored_individuals[0:self.mu]

    def on_result(self, fitness, fargs, individual, **kwargs):
        scored_individual = (individual, fitness)
        _, best_fitness = self.best_scored_individual

        if best_fitness is None or fitness < best_fitness:
            self.best_scored_individual = scored_individual

    def on_error(self, error, fargs, individual, **kwargs):
        pass