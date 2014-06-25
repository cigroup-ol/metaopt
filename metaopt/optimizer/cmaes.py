# -*- coding: utf-8 -*-
"""
Optimizer implementing the (mu, lambda)-CMA-ES.

http://www.lri.fr/~hansen/gecco2013-CMA-ES-tutorial.pdf
http://www.lri.fr/~hansen/cmatutorial.pdf
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from math import exp
from random import gauss, sample
from copy import deepcopy

# First Party
from metaopt.core.arg.util.creator import ArgsCreator
from metaopt.optimizer.optimizer import Optimizer
from metaopt.core.optimize.util.exception import WrongArgumentTypeException
from metaopt.core.optimize.util.exception import MissingRequirementsException
from metaopt.core.stoppable.util.exception import StoppedError

try:
    # Numpy
    from numpy import array, mean, log, eye, diag, transpose
    from numpy import identity, matrix, dot, exp, zeros, ones, sqrt
    from numpy.random import normal, rand
    from numpy.linalg import eigh, norm
except ImportError:
    raise MissingRequirementsException('NumPy')

try:
    xrange  # will work in python2, only @UndefinedVariable
except NameError:
    xrange = range  # rename range to xrange in python3

class CMAESOptimizer(Optimizer):
    """
    Optimization based on the (mu, lambda)-CMA-ES.

    This optimizer should be combined with a global timeout, otherwise it will
    run indefinitely.
    """

    MU = 15
    LAMBDA = 100
    STEP_SIZE = 1.0

    def __init__(self, mu=MU, lamb=LAMBDA, global_step_size=STEP_SIZE):
        super(CMAESOptimizer, self).__init__()

        self.population = []
        self.scored_population = []
        self.best_scored_indivual = (None, None)

        self.aborted = False
        self.generation = 1

        self._mu = mu
        self._lambd = lamb
        self._sigma = global_step_size

    def optimize(self, invoker, param_spec, return_spec=None, minimize=True):
        del return_spec
        del minimize

        # param constraint check
        for param in param_spec.params.values():
            if not param.type == 'float':
                raise WrongArgumentTypeException()

        self._invoker = invoker
        self.param_spec = param_spec

        args_creator = ArgsCreator(self.param_spec)

        # dimensions for equation setup
        self._n = len(args_creator.random())

        # start position as numpy array, numpify
        start = args_creator.random()
        self._xmean = array(map(lambda arg : arg.value, start))

        # initialize the parameters with member variables
        self.initialize_parameters()

        while not self.exit_condition():
            self.add_offspring()
            self.score_population()

            if self.aborted:
                return self.best_scored_indivual[0]

            self.select_parents()
            self.generation += 1

        return self.best_scored_indivual[0]

    def initialize_parameters(self):
        # alias
        n = self._n

        # recombination weights
        self._weights = [log(self._mu + 0.5) - log(i + 1) for i in range(self._mu)]

        # normalize recombination weights array
        self._weights = [w / sum(self._weights) for w in self._weights]

        # variance-effectiveness of sum w_i x_i
        self._mueff = sum(self._weights) ** 2 / sum(w ** 2 for w in self._weights)

        # time constant for cumulation for C
        self._cc = (4 + self._mueff / n) / (n + 4 + 2 * self._mueff / n)

        # t-const for cumulation for sigma control
        self._cs = (self._mueff + 2) / (n + self._mueff + 5)

        # learning rate for rank-one update of C
        self._c1 = 2 / ((n + 1.3) ** 2 + self._mueff)

        # and for rank-mu update
        term_a = 1 - self._c1
        term_b = 2 * (self._mueff - 2 + 1 / self._mueff) / ((n + 2) ** 2 + self._mueff)
        self._cmu = min(term_a, term_b)

        # damping for sigma, usually close to 1
        self._damps = 2 * self._mueff / self._lambd + 0.3 + self._cs

        # evolution paths for C and sigma
        self._pc = zeros(n)
        self._ps = zeros(n)

        # B-matrix of eigenvectors, defines the coordinate system
        self._B = identity(n)

        # diagonal matrix of eigenvalues (sigmas of axes)
        self._D = ones(n)  # diagonal D defines the scaling

        # covariance matrix, rotation of mutation ellipsoid
        self._C = identity(n)
        self._invsqrtC = identity(n)  # C^-1/2

        # approx. norm of random vector
        self._norm = sqrt(n) * (1.0 - (1.0/(4*n)) + (1.0/(21*n**2)))

        # first run
        self._D, self._B = eigh(self._C)
        self._B = matrix(self._B)
        self._D = [d ** 0.5 for d in self._D]

        invD = diag([1.0/d for d in self._D])
        self._invsqrtC = self._B * invD * transpose(self._B)

    def exit_condition(self):
        pass

    def limit_to_interval(self, x):
        params = self.param_spec.params.values()
        for i, param in enumerate(params):
            if x[0, i] < param.lower_bound:
                x[0, i] = param.lower_bound
            elif x[0, i] > param.upper_bound:
                x[0, i] = param.upper_bound
        return x

    def add_offspring(self):
        for _ in xrange(self._lambd):
            normals = transpose(matrix([normal(0.0, d) for d in self._D]))
            value = self._xmean + transpose(self._sigma * self._B * normals)
            value = self.limit_to_interval(value)
            self.population.append(value)

    def score_population(self):
        self.scored_population = []

        for individual in self.population:
            # metaoptify
            args_creator = ArgsCreator(self.param_spec)
            individual = individual.getA1().tolist()
            individual = args_creator.args(individual)
            args = individual

            try:
                self._invoker.invoke(caller=self, fargs=args,
                                     individual=individual)
            except StoppedError:
                self.aborted = True
                break

        self._invoker.wait()

    def select_parents(self):
        self.scored_population.sort(key=lambda s: s[1])
        new_scored_population = self.scored_population[0:self._mu]
        values = map(lambda s: s[0], new_scored_population)

        # numpify
        numpify = lambda val : array(map(lambda arg : arg.value, val))
        values = map(numpify, values)

        # alias
        n = self._n

        # remember old xmean for parameter adjustment
        oldxmean = deepcopy(self._xmean)

        # calculate new xmean
        self._xmean = matrix([[0.0 for i in range(0,n)]])
        weighted_values = zip(self._weights, values)
        for weight, value in weighted_values:
            self._xmean += weight * value

        # cumulation: update evolution paths
        y = self._xmean - oldxmean
        z = dot(self._invsqrtC, y.T) # C**(-1/2) * (xnew - xold)

        # normalizing coefficient c and evolution path sigma control
        c = (self._cs * (2 - self._cs) * self._mueff) ** 0.5 / self._sigma
        self._ps = (1 - self._cs) * self._ps + c * z

        # normalizing coefficient c and evolution path for rank-one-update
        # without hsig (!)
        c = (self._cc * (2 - self._cc) * self._mueff) ** 0.5 / self._sigma
        self._pc = (1 - self._cc) * self._pc + c * y

        # adapt covariance matrix C
        # rank one update term
        term_cov1 = self._c1 * (transpose(matrix(self._pc)) * matrix(self._pc))

        # ranke mu update term
        valuesv = [(value - oldxmean) / self._sigma for value in values]
        term_covmu = self._cmu *\
            sum([self._weights[i] * (transpose(matrix(valuesv[i])) *\
            matrix(valuesv[i]))\
            for i in range(0, self._mu)])

        self._C = (1 - self._c1 - self._cmu) * self._C + term_cov1 + term_covmu

        # update global sigma by comparing evolution path
        # with approx. norm of random vector
        self._sigma *= exp(self._cs / self._damps) *\
            ((norm(self._ps.getA1()) / self._norm) - 1)

        # calculate new matrices
        self._D, self._B = eigh(self._C)
        self._B = matrix(self._B)
        self._D = [d ** 0.5 for d in self._D]

        invD = diag([1.0/d for d in self._D])
        self._invsqrtC = self._B * invD * transpose(self._B)

    def on_result(self, value, fargs, individual, **kwargs):
        del fargs
        del kwargs
        # _, fitness = result
        fitness = value
        scored_individual = (individual, fitness)
        self.scored_population.append(scored_individual)

        _, best_fitness = self.best_scored_indivual

        if best_fitness is None or fitness < best_fitness:
            self.best_scored_indivual = scored_individual

    def on_error(self, value, fargs, individual, **kwargs):
        del value  # TODO
        del fargs  # TODO
        del individual  # TODO
        del kwargs  # TODO
