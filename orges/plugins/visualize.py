# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

import matplotlib.pyplot as plt

from orges.plugins.dummy import DummyPlugin


class VisualizeLandscapePlugin(DummyPlugin):
    def __init__(self):
        self.individuals = []
        self.fitnesses = []

    def setup(self, f, param_spec, return_spec):
        del f, param_spec
        self.return_spec = return_spec

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

        z_label = self.return_spec.return_values[0]["name"]
        ax.set_zlabel(z_label)

        X = map(lambda individual: individual[0].value, self.individuals)
        Y = map(lambda individual: individual[1].value, self.individuals)
        Z = self.fitnesses

        ax.scatter(X, Y, Z)
        plt.show()


class VisualizeBestFitnessPlugin(DummyPlugin):
    def __init__(self):
        self.best_fitnesses = []
        self.current_best = None

    def setup(self, f, param_spec, return_spec):
        del f, param_spec
        self.return_spec = return_spec

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

        y_label = self.return_spec.return_values[0]["name"]
        ax.set_ylabel(y_label)

        ax.plot(self.best_fitnesses)
        plt.show()
