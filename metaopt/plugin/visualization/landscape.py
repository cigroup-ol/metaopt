# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # Load 3d plots capabilities
from numpy import meshgrid
from scipy.interpolate import griddata

# First Party
from metaopt.plugin.plugin import Plugin


NUMBER_OF_SAMPLES = 200

COLORMAP = cm.jet
REVERSED_COLORMAP = cm.jet_r


class VisualizeLandscapePlugin(Plugin):
    def __init__(self, x_param_index=0, y_param_index=1):
        """Visualize fitness landscape"""
        super(VisualizeLandscapePlugin, self).__init__()

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
        self.fitnesses.append(fitness.raw_values)

        if not self.best_fitness or fitness < self.best_fitness:
            self.best_fitness = fitness

        if not self.worst_fitness or fitness > self.worst_fitness:
            self.worst_fitness = fitness

    def show_image_plot(self):
        """Show an image plot"""
        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.set_xlabel(self.get_x_label())
        ax.set_ylabel(self.get_y_label())

        x = map(lambda individual: individual[self.x_param_index].value,
                self.individuals)

        y = map(lambda individual: individual[self.y_param_index].value,
                self.individuals)

        xi = np.linspace(*self.get_x_interval(), num=NUMBER_OF_SAMPLES)
        yi = np.linspace(*self.get_y_interval(), num=NUMBER_OF_SAMPLES)

        X, Y = meshgrid(xi, yi)
        Z = griddata((x, y), self.fitnesses, (X, Y))

        vmax = max(self.best_fitness.raw_values, self.worst_fitness.raw_values)
        vmin = min(self.best_fitness.raw_values, self.worst_fitness.raw_values)

        cmap = self.choose_colormap()

        extent = (
            self.get_x_interval()[0], self.get_x_interval()[1],
            self.get_y_interval()[0], self.get_y_interval()[1],
        )

        img = ax.imshow(Z, cmap=cmap, extent=extent, vmax=vmax, vmin=vmin,
                        origin="lower")

        plt.colorbar(img)
        plt.show()

    def show_surface_plot(self):
        """Show a surface plot"""
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

        vmax = max(self.best_fitness.raw_values, self.worst_fitness.raw_values)
        vmin = min(self.best_fitness.raw_values, self.worst_fitness.raw_values)

        cmap = self.choose_colormap()
        ax.plot_surface(X, Y, Z, cmap=cmap, vmax=vmax, vmin=vmin)

        plt.show()

    def choose_colormap(self):
        if self.is_minimization():
            return REVERSED_COLORMAP
        else:
            return COLORMAP

    def is_minimization(self):
        return self.return_spec.return_values[0]["minimize"]

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
