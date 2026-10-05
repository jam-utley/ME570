'''
Class and test data for graphs
'''

import pickle
from math import isnan, pi

import numpy as np
from matplotlib import pyplot as plt

import me570_geometry


def graph_test_data_load(variable_name):
    """
    Loads data from the file graph_test_data.pkl.
    """
    with open('graph_test_data.pkl', 'rb') as fid:
        saved_data = pickle.load(fid)
    if variable_name is None:
        for key in saved_data.keys():
            print(key)
    else:
        return Graph(saved_data[variable_name])


def graph_test_data_plot():
    """
    Plot two solved graphs
    """

    for name, idx_goal in [('graphVector_solved', 3),
                           ('graphVectorMedium_solved', 14)]:
        graph = Graph(graph_test_data_load(name))
        plt.figure()
        graph.plot(flag_heuristic=True, idx_goal=idx_goal)
        plt.title(name)


def plot_arrows_from_list(arrow_list, scale=1.0, color=(0., 0., 0.)):
    """
    Plot arrows from a list of pairs of base points and displacements
    """
    if len(arrow_list) > 0:
        x_edges, v_edges = [np.hstack(x) for x in zip(*arrow_list)]
        plt.quiver(x_edges[0, :],
                   x_edges[1, :],
                   v_edges[0, :],
                   v_edges[1, :],
                   angles='xy',
                   scale_units='xy',
                   scale=scale,
                   color=color)


def plot_text(coord, str_label, color=(1., 1., 1.)):
    """
    Wrap plt.text to get a consistent look
    """
    plt.text(coord[0].item(),
             coord[1].item(),
             str_label,
             ha='center',
             va='center',
             fontsize='xx-small',
             bbox={
                 'boxstyle': 'round',
                 'fc': color,
                 'ec': None
             })


class Graph:
    """
    A class collecting a  graph_vector data structure and all the functions that operate on a graph.
    """

    def __init__(self, graph_vector):
        """
        Stores the arguments as internal attributes.
        """
        self.graph_vector = graph_vector
        self.idx_closed = []

    def _apply_neighbor_function(self, func):
        """
        Apply a function on each node and chain the result
        """
        list_of_lists = [func(n) for n in self.graph_vector]
        return [e for l in list_of_lists for e in l]

    def _neighbor_weights_with_positions(self, n_current):
        """
        Get all weights and where to display them
        """
        x_current = n_current['x']
        return [
            (weight_neighbor,
             self.graph_vector[idx_neighbor]['x'] * 0.25 + x_current * 0.75)
            for (weight_neighbor, idx_neighbor
                 ) in zip(n_current['neighbors_cost'], n_current['neighbors'])
        ]

    def _neighbor_displacements(self, n_current):
        """
        Get all displacements with respect to the neighbors for a given node
        """
        x_current = n_current['x']
        return [(x_current, self.graph_vector[idx_neighbor]['x'] - x_current)
                for idx_neighbor in n_current['neighbors']]

    def _neighbor_backpointers(self, n_current):
        """
        Get coordinates for backpointer arrows
        """
        x_current = n_current['x']
        idx_backpointer = n_current.get('backpointer', None)
        if idx_backpointer is not None:
            arrow = [
                (x_current,
                 0.5 * (self.graph_vector[idx_backpointer]['x'] - x_current))
            ]
        else:
            arrow = []
        return arrow

    def _neighbor_backpointers_cost(self, n_current):
        """
        Get value and coordinates for backpointer costs
        """
        x_current = n_current['x']
        idx_backpointer = n_current.get('backpointer', None)
        pos = 0
        if idx_backpointer is not None:
            arrow = [(n_current['g'],
                      self.graph_vector[idx_backpointer]['x'] * pos +
                      x_current * (1. - pos))]
        else:
            arrow = []
        return arrow

    def has_backpointers(self):
        """
        Return True if self.graph_vector has a "backpointer" field
        """
        return self.graph_vector is not None and len(
            self.graph_vector) > 0 and 'backpointer' in self.graph_vector[0]

    def plot(self,
             flag_edges=True,
             flag_nodes=True,
             flag_labels=False,
             flag_edge_weights=False,
             flag_backpointers=True,
             flag_backpointers_cost=True,
             flag_heuristic=False,
             flag_axis_limits=True,
             node_lists=None,
             idx_closed=None,
             idx_goal=None,
             idx_best=None):
        """
        The function plots the contents of the graph described by the
        graph_vector structure, alongside other related, optional data.
        """

        if flag_edges:
            displacement_list = self._apply_neighbor_function(
                self._neighbor_displacements)
            plot_arrows_from_list(displacement_list, scale=1.05)

        if flag_labels:
            for idx, n_current in enumerate(self.graph_vector):
                x_current = n_current['x']
                plot_text(x_current, str(idx))

        if idx_closed is not None:
            for idx in idx_closed:
                x_current = self.graph_vector[idx]['x']
                plt.scatter(x_current[0],
                            x_current[1],
                            marker='s',
                            color=(0., 0., 1.))

        if idx_goal is not None:
            x_goal = self.graph_vector[idx_goal]['x']
            plt.plot(x_goal[0, :],
                     x_goal[1, :],
                     marker='d',
                     markersize=10,
                     color=(.8, .1, .1))

        if idx_best is not None:
            x_best = self.graph_vector[idx_best]['x']
            plt.plot(x_best[0, :],
                     x_best[1, :],
                     marker='d',
                     markersize=10,
                     color=(0., 1., 0.))

        if flag_heuristic and idx_goal is not None:
            for idx, n_current in enumerate(self.graph_vector):
                x_current = n_current['x']
                h_current = self.heuristic(idx, idx_goal)
                plot_text(x_current, f'h={h_current:.2f}', color=(.8, 1., .8))
                if flag_heuristic and idx_goal is not None:
                    idx_backpointer = n_current.get('backpointer', None)
                    if idx_backpointer is not None:
                        cost = n_current['g'] + h_current
                        offset = np.array([[0], [.15]])
                        plot_text(x_current + offset,
                                  f'f={cost:.2f}',
                                  color=(.8, 1., .8))

        if flag_edge_weights:
            weight_list = self._apply_neighbor_function(
                self._neighbor_weights_with_positions)
            for (weight, coord) in weight_list:
                plot_text(coord, str(weight), color=(.8, .8, 1.))

        if flag_backpointers and self.has_backpointers():
            backpointer_arrow_list = self._apply_neighbor_function(
                self._neighbor_backpointers)
            plot_arrows_from_list(backpointer_arrow_list,
                                  scale=1.05,
                                  color=(0.1, .8, 0.1))

        if flag_backpointers_cost and self.has_backpointers:
            backpointer_cost_list = self._apply_neighbor_function(
                self._neighbor_backpointers_cost)
            offset = np.array([[0], [-.15]])
            for (cost, coord) in backpointer_cost_list:
                plot_text(coord + offset, f'g={cost:.2f}', color=(.8, 1., .8))

        if node_lists is not None:
            if not isinstance(node_lists[0], list):
                node_lists = [node_lists]
            markers = ['d', 'o', 's', '*', 'h', '^', '8']
            for i, lst in enumerate(node_lists):
                x_list = [self.graph_vector[e]['x'] for e in lst]
                coords = np.hstack(x_list)
                plt.plot(
                    coords[0, :],
                    coords[1, :],
                    markers[i % len(markers)],
                    markersize=10,
                )
        if flag_nodes:
            x_list = [n['x'] for n in self.graph_vector]
            coords = np.hstack(x_list)
            plt.plot(coords[0, :], coords[1, :], 'x')
        if flag_axis_limits:
            coords_x = [n['x'][0].item() for n in self.graph_vector]
            x_min, x_max = min(coords_x), max(coords_x)
            x_lim = [
                x_min - (x_max - x_min) * 0.01,
                x_max + (x_max - x_min) * 0.01,
            ]
            coords_y = [n['x'][0].item() for n in self.graph_vector]
            y_min, y_max = min(coords_y), max(coords_y)
            y_lim = [
                y_min - (y_max - y_min) * 0.01,
                y_max + (y_max - y_min) * 0.01,
            ]
            ax = plt.gca()
            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)

    def nearest_neighbors(self, x_query, k_nearest):
        """
        Returns the k nearest neighbors in the graph for a given point.
        """

        x_graph = np.hstack([n['x'] for n in self.graph_vector])
        distances_squared = np.sum((x_graph - x_query)**2, 0)
        idx = np.argpartition(distances_squared, k_nearest)
        return idx[:k_nearest]
