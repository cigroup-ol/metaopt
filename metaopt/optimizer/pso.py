# -*- coding: utf-8 -*-
"""
Particle Swarm Optimizer (PSO)
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# First Party
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.optimizer.optimizer import Optimizer
from metaopt.core.optimize.util.exception import WrongArgumentTypeException
from metaopt.core.stoppable.util.exception import StoppedError

try:
    # Numpy
    from numpy import array
    from numpy.random import normal
except ImportError:
    raise MissingRequirementsException('NumPy')

try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3

class PSOOptimizer(Optimizer):
    """
    Optimization based on the general PSO.

    This optimizer should be combined with a global timeout, otherwise it will
    run indefinitely.
    """

    LAMBDA = 100
    C_1 = 0.5
    C_2 = 0.5
    INERTIA_WEIGHT = 0.5
    SPEED = 1.0

    def __init__(self, lamb=LAMBDA, c1=C_1, c2=C_2,
                 inertia_weight=INERTIA_WEIGHT, speed=SPEED):
        super(PSOOptimizer, self).__init__()

        self.population = []
        self.aborted = False
        self.generation = 1

        self._lambd = lamb
        self._c1 = c1
        self._c2 = c2
        self._inertia_weight = inertia_weight
        self._speed = speed

    def optimize(self, invoker, param_spec, return_spec=None):
        del return_spec

        # param constraint check
        for param in param_spec.params.values():
            if not param.type == 'float':
                raise WrongArgumentTypeException()

        self._invoker = invoker
        self.param_spec = param_spec

        args_creator = ArgsCreator(self.param_spec)
        dims = len(args_creator.random())

        # initialize population
        while len(self.population) < self._lambd:
            pos = args_creator.random() # numpify
            pos = array(map(lambda arg : arg.value, pos))
            velocity = array([self._speed] * dims)
            particle = pos, velocity
            self.population.append(particle)

        while not self.exit_condition():
            if self.aborted:
                return args_creator.args(self.best_gpos)

            self.score_population()
            self.update()
            self.generation += 1

        return args_creator.args(self.best_gpos)

    def score_population(self):
        self.scored_population = []

        for particle in self.population:
            # metaoptify
            args_creator = ArgsCreator(self.param_spec)
            pos = particle[0].tolist()
            pos = args_creator.args(pos)

            try:
                self._invoker.invoke(caller=self, fargs=pos,
                                     individual=particle)
            except StoppedError:
                self.aborted = True
                break

        self._invoker.wait()

    def exit_condition(self):
        pass

    def limit_to_interval(self, x):
        params = self.param_spec.params.values()
        for i, param in enumerate(params):
            if x[i] < param.lower_bound:
                x[i] = param.lower_bound
            elif x[i] > param.upper_bound:
                x[i] = param.upper_bound
        return x

    def update(self):
        self.scored_population.sort(key=lambda s : s[1])

        # global best
        self.best_gpos = self.scored_population[0][0][0]
        self.best_fitness = self.scored_population[0][1]

        # update particles
        for particle, fitness in self.scored_population:

            if len(particle) < 3:
                pos, vel = particle
                best_pos = pos
                best_fitness = fitness
            else:
                pos, vel, best_fitness, best_pos = particle

            # update the best_pos, best_fitness
            # when better fitness
            if fitness < best_fitness:
                best_pos = pos
                best_fitness = fitness

            # alias
            iw, c1, c2 = self._inertia_weight, self._c1, self._c2
            bpp, bgp = best_pos, self.best_gpos

            # direction vectors
            bppvec, bgpvec = bpp - pos, bgp - pos

            # mutation
            r1, r2 = normal(1), normal(1)

            # update the velocity
            vel = iw * vel + c1 * r1 * bppvec + c2 * r2 * bgpvec

            # update the position
            pos = self.limit_to_interval(vel * pos)

        # copy population
        self.population = map(lambda s : s[0], self.scored_population)

    def on_error(self, value, fargs, **kwargs):
        pass

    def on_result(self, value, fargs, individual, **kwargs):
        del fargs
        del kwargs
        # _, fitness = result
        fitness = value
        scored_individual = (individual, fitness)

        self.scored_population.append(scored_individual)

