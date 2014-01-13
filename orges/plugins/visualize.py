# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

import matplotlib.pyplot as plt

from orges.plugins.dummy import DummyPlugin


class VisualizeLandscapePlugin(DummyPlugin):
    def __init__(self):
        self.individuals = []
        self.fitnesses = []

    def on_invoke(self, invocation):
        pass

    def on_result(self, invocation):
        self.individuals.append(invocation.fargs)
        self.fitnesses.append(invocation.current_result)

    def on_error(self, invocation):
        pass

    def save_visualization(self):
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlabel(self.individuals[0][0].param.title)
        ax.set_ylabel(self.individuals[0][1].param.title)
        ax.set_zlabel("Fitness")

        X = map(lambda individual: individual[0].value, self.individuals)
        Y = map(lambda individual: individual[1].value, self.individuals)
        Z = self.fitnesses

        ax.scatter(X, Y, Z)
        plt.show()

class VisualizeBestFitnessPlugin(DummyPlugin):
    def __init__(self):
        self.best_fitnesses = []
        self.current_best = None

    def on_invoke(self, invocation):
        pass

    def on_result(self, invocation):
        fitness = invocation.current_result

        if self.current_best is None or fitness < self.current_best:
            self.current_best = fitness

        self.best_fitnesses.append(self.current_best)

    def on_error(self, invocation):
        pass

    def save_visualization(self):
        fig = plt.figure()

        ax = fig.add_subplot(111)
        ax.set_xlabel("Number of Invocations")
        ax.set_ylabel("Fitness")

        ax.plot(self.best_fitnesses)
        plt.show()
