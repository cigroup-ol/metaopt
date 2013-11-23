# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

from random import sample

from orges.args import ArgsCreator, default_mutation_stength
from orges.optimizer.base import BaseOptimizer, BaseCaller


class RechenbergOptimizer(BaseOptimizer, BaseCaller):
    # TODO: Find good default values
    MU = 3
    LAMBDA = 3
    A = 0.1

    def __init__(self, mu=MU, lamb=LAMBDA, a=A):
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

    @property
    def invoker(self):
        return self._invoker

    @invoker.setter
    def invoker(self, invoker):
        invoker.caller = self
        self._invoker = invoker

    def optimize(self, f, param_spec, return_spec=None, minimize=True):
        self.f = f
        self.param_spec = param_spec

        params = param_spec.params.values()
        self.sigmas = [default_mutation_stength(param) for param in params]

        self.initalize_population()
        self.score_population()

        while not self.exit_condition():
            self.add_offspring()
            self.score_population()
            self.select_parents()
            self.change_mutation_strength()

            self.previous_best_fitness  = self.best_fitness
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
            self.invoker.invoke(self.f, individual, individual=individual)

        self._invoker.wait()

    def select_parents(self):
        self.scored_population.sort(key=lambda s: s[1])
        new_scored_population = self.scored_population[0:self.mu]
        self.population = map(lambda s: s[0], new_scored_population)

    def change_mutation_strength(self):
        if self.previous_best_fitness is None:
            return # We can't estimate success probablity yet

        successes = len(filter(lambda scored: scored[1] <
            self.previous_best_fitness, self.scored_population))

        probablity = successes / self.lamb

        # TODO: What happens if sigmas get too large or small
        if probablity > 1/5:
            self.sigmas = map(lambda sigma: sigma / self.a, self.sigmas)
        elif probablity < 1/5:
            self.sigmas = map(lambda sigma: sigma * self.a, self.sigmas)

        print(self.sigmas)

    def on_result(self, result, args, individual):
        # _, fitness = result
        fitness = result
        scored_individual = (individual, fitness)
        self.scored_population.append(scored_individual)

        best_individual, best_fitness = self.best_scored_indivual

        if best_fitness is None or fitness < best_fitness:
            self.best_scored_indivual = scored_individual
            self.best_fitness = fitness

    def on_error(self, args, individual):
        pass
