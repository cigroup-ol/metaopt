# -*- coding: utf-8 -*-
# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Standard Library
from datetime import datetime

# Third Party
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # Load 3d plots capabilities

# First Party
from metaopt.plugin.plugin import Plugin


NUMBER_OF_SAMPLES = 200

COLORMAP = cm.jet
REVERSED_COLORMAP = cm.jet_r


class VisualizeBestFitnessPlugin(Plugin):
    """Visualize optimization progess"""
    def __init__(self):
        self.best_fitnesses = []
        self.timestamps = []

        self.start_time = None
        self.current_best = None
        self.return_spec = None

    def setup(self, f, param_spec, return_spec):
        del f, param_spec
        self.return_spec = return_spec

        if not self.start_time:
            self.start_time = datetime.now()

    def on_result(self, invocation):
        fitness = invocation.current_result

        if self.current_best is None or fitness < self.current_best:
            self.current_best = fitness

        self.best_fitnesses.append(self.current_best.raw_values)

        time_delta = datetime.now() - self.start_time
        self.timestamps.append(time_delta.total_seconds())

    def show_fitness_invocations_plot(self):
        """Show a fitness--invocations plot"""
        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.set_xlabel("Number of Invocations")
        ax.set_ylabel(self.get_y_label())

        ax.plot(self.best_fitnesses)
        plt.show()

    def show_fitness_time_plot(self):
        """Show a fitness--time plot"""
        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.set_xlabel("Time")
        ax.set_ylabel(self.get_y_label())

        ax.plot(self.timestamps, self.best_fitnesses)
        plt.show()

    def get_y_label(self):
        return self.return_spec.return_values[0]["name"]
