from __future__ import division
from __future__ import print_function
from __future__ import with_statement

from numpy.random import randn
from numpy import abs
from random import sample
from numpy import exp


def f(args):
    mu = args['mu']
    lambd = args['lambd']
    d = args['d']
    tau0 = args['tau0']
    tau1 = args['tau1']
    epsilon = args['epsilon']

    optimum = 0
    population = []
    sigma = randn(d)

    def fitness(x):
        return (x, (x[0] ** 2).sum())

    for i in range(lambd):
        population.append((randn(d), sigma))

    fitvals = map(fitness, population)
    fitvals = sorted(fitvals, key=lambda t: t[1])

    best = fitvals[0]
    generations = 0

    while abs(optimum - best[1]) > epsilon:
        offspring = []
        for i in range(lambd):
            parents = sample(population, 2)

                        # recombination
            child = (0.5 * parents[0][0] + 0.5 * parents[1][0],
                             0.5 * (parents[0][1] + parents[1][1]))

            tau0_random = randn(1)
            # mutation of position
            for i in range(child[0].shape[0]):
                child[0][i] += randn(1) * child[1][i]
                child[1][i] *= exp(tau0 * tau0_random) * exp(tau1 * randn(1))

            offspring.append(child)

        all_population = offspring + population

        fitvals = map(fitness, all_population)
        fitvals = sorted(fitvals, key=lambda t: t[1])

        best = fitvals[0]
        population = [x[0] for x in fitvals[0:mu]]
        generations += 1

    return generations

args = {
    'mu': 15,
    'lambd': 100,
    'd': 2,
    'tau0': 0.5,
    'tau1': 0.6,
    'epsilon': 0.0001,
}

# for tau0 in [i / 10.0 for i in range(10)]:
#     args_current = deepcopy(args)
#     args_current['tau0'] = tau0
#     print "tau0: %f, generations: %i" % (tau0, optimize(args))

if __name__ == '__main__':
    print(f(args))
