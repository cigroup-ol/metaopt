# -*- coding: utf-8 -*-
from __future__ import division, print_function, with_statement

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # Load 3d plots capabilities
from numpy import meshgrid
from scipy.interpolate import griddata

from orges.plugins.dummy import DummyPlugin

NUMBER_OF_SAMPLES = 200

class VisualizeLandscapePlugin(DummyPlugin):
    def __init__(self, x_param_index=0, y_param_index=1):
        self.x_param_index = x_param_index
        self.y_param_index = y_param_index

        self.individuals = []
        self.fitnesses = []

        self.best_fitness = None
        self.worst_fitness = None

        self.param_spec = None
        self.return_spec = None

    def setup(self, f, param_spec, return_spec):
        del f
        self.param_spec = param_spec
        self.return_spec = return_spec

    def on_result(self, invocation):
        self.individuals.append(invocation.fargs)

        fitness = invocation.current_result
        self.fitnesses.append(fitness)

        if not self.best_fitness or fitness < self.best_fitness:
            self.best_fitness = fitness

        if not self.worst_fitness or fitness > self.worst_fitness:
            self.worst_fitness = fitness

    def save_visualization(self):
        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlabel(self.get_x_label())
        ax.set_ylabel(self.get_y_label())
        ax.set_zlabel(self.get_z_label())

        x = map(lambda individual: individual[self.x_param_index].value,
                self.individuals)

        y = map(lambda individual: individual[self.y_param_index].value,
                self.individuals)

        xi = np.linspace(*self.get_x_interval(), num=NUMBER_OF_SAMPLES)
        yi = np.linspace(*self.get_y_interval(), num=NUMBER_OF_SAMPLES)

        X, Y = meshgrid(xi, yi)
        Z = griddata((x, y), self.fitnesses, (X, Y))

        vmax = max(self.best_fitness, self.worst_fitness)
        vmin = min(self.best_fitness, self.worst_fitness)

        ax.plot_surface(X, Y, Z, cmap=cm.jet, vmax=vmax, vmin=vmin)

        plt.show()

    def get_x_label(self):
        return self.param_spec.params.values()[self.x_param_index].title

    def get_y_label(self):
        return self.param_spec.params.values()[self.y_param_index].title

    def get_z_label(self):
        return self.return_spec.return_values[0]["name"]

    def get_x_interval(self):
        return self.param_spec.params.values()[self.x_param_index].interval

    def get_y_interval(self):
        return self.param_spec.params.values()[self.y_param_index].interval


class VisualizeBestFitnessPlugin(DummyPlugin):
    def __init__(self):
        self.best_fitnesses = []
        self.current_best = None

    def setup(self, f, param_spec, return_spec):
        del f, param_spec
        self.return_spec = return_spec

    def on_result(self, invocation):
        fitness = invocation.current_result

        if self.current_best is None or fitness < self.current_best:
            self.current_best = fitness

        self.best_fitnesses.append(self.current_best)

    def save_visualization(self):
        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.set_xlabel("Number of Invocations")
        ax.set_ylabel(self.get_y_label())

        ax.plot(self.best_fitnesses)
        plt.show()

    def get_y_label(self):
        return self.return_spec.return_values[0]["name"]
