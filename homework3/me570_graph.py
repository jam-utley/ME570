"""
Class and test data for graphs
"""
from math import isnan, pi
import numpy as np
from matplotlib import pyplot as plt
import me570_geometry
import me570_pq
import pickle


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
    A class collecting a  graph_vector data structure and all the functions
    that operate on a graph.
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

    def heuristic(self, idx_x, idx_goal):
        """
        Computes the heuristic h given by the Euclidean distance between the
        nodes with indexes idx_x and   idx_goal.
        """
        x_node = self.graph_vector[idx_x]['x']
        x_goal = self.graph_vector[idx_goal]['x']
        h_val = np.linalg.norm(x_goal-x_node)

        return h_val

    def get_expand_list(self, idx_n_best, idx_closed):
        """
        Finds the neighbors of element idx_n_best that are not in idx_closed
        (line it:expand in Algorithm~ alg:astar).
        """
        #pass  # Substitute with your code
        # Question 1.2 CODE
        # Reference pseudo-code: Algorithm 1, line 11
        # Find nearest neighbors of idx_n_best that are NOT in idx_closed
        # idx_expand = array of indices of the neighbors of element idx_n_best
        # in graph_vector

        #Get neighbors of idx_n_best
        neighbors = self.graph_vector[idx_n_best]['neighbors']
        #idx_expand are indexes of neighbors NOT in closed list
        idx_expand = [i for i in neighbors if i not in idx_closed]
        return idx_expand

    def expand_element(self, idx_n_best, idx_x, idx_goal, pq_open):
        """
        This function expands the vertex with index idx_x (which is a neighbor
        of the one with index   idx_n_best) and updates the attribute
        graph_vector and returns an updated version of   pq_open.
        """
        #pass  # Substitute with your code
        # Question 1.3
        # if idx_x is not in pq_open:
        n_best = self.graph_vector[idx_n_best]
        pos = list(n_best['neighbors']).index(idx_x)
        cost = n_best['neighbors_cost'][pos]
        if pq_open.is_member(idx_x) is not True:
            # Set Backpointer cost
            # (g(idx_x)=g(idx_n_best)+c((idx_n_best,idx_x)))
            self.graph_vector[idx_x]['g'] = n_best['g'] + cost
            # set backpointer of x to n_best
            self.graph_vector[idx_x]['backpointer'] = idx_n_best
            # compute heuristic h(idx_x)
            heuristic = Graph.heuristic(self, idx_x, idx_goal)
            # add f(x) = g(idx_x) + h(idx_x) to pq_open
            f_of_x = self.graph_vector[idx_x]['g'] + heuristic
            pq_open.push(idx_x, f_of_x)
        # else if g(idx_n_best)+c(idx_n_best,idx_x)<g(idx_x):
        elif (n_best['g'] + cost < self.graph_vector[idx_x]['g']):
            # update backpointer cost
            # g(idx_x) = g(idx_n_best)+c(idx_n_best,idx_x)
            self.graph_vector[idx_x]['g']=(self.graph_vector[idx_n_best]['g']
                                           + cost)
            # update backpointer of idx_x to idx_n_best

            self.graph_vector[idx_x]['backpointer'] = idx_n_best
            pq_open.push(idx_x, self.graph_vector[idx_x]['g']
                         + self.heuristic(idx_x, idx_goal))
        return pq_open

    def path(self, idx_start, idx_goal):
        """
        This function follows the backpointers from the node with index
        idx_goal in   graph_vector to the one with index   idx_start node, and
        returns the  coordinates (not indexes) of the sequence of traversed
        elements.
        """
        #pass  # Substitute with your code
        # Question 1.4
        # x_path is 2 x nb_path array
        # Each row contains the COORDINATES of a points from goal to start
        # In reverse order.
        # x_path[:,0]=graph_vector[idx_start]['x']
        # x_path[:,-1] = graph_vector[idx_goal]['x']
        # Will have to use some 'self' stored variables to access backpointers
        #x_path = []
        idx = idx_goal
        backpointer = self.graph_vector[idx_goal]['backpointer']
        #cost = self.graph_vector[idx_goal]['g']
        x_list = [self.graph_vector[idx]['x']]
        #x_path.append((idx, cost))
        while idx != idx_start:
            idx = self.graph_vector[idx]['backpointer']
            backpointer = self.graph_vector[backpointer]['backpointer']
            x_list.append(self.graph_vector[idx]['x'])
        x_path = np.hstack(x_list[::-1])
        return x_path

    def search(self, idx_start, idx_goal):
        """
        Implements the  A^* algorithm, as described by the pseudo-code in
        Algorithm~ alg:astar.
        """
        # pass  # Substitute with your code
        # Question 1.5
        # Required elements: pq_open, idx_closed

        # Structure -

        # Initialization
        # Add idx_start to pq_open, backpointer cost = 0 (bc at the start)
        # Initialize idx_closed to be empty
        self.graph_vector[idx_start]['backpointer'] = None
        self.graph_vector[idx_start]['g'] = 0
        pq_open = me570_pq.PriorityQueue()
        pq_open.push(idx_start, self.heuristic(idx_start, idx_goal)) # f=g+h
        idx_closed = []

        # Loop
        while not pq_open.is_empty():
            # Pick idx_n_best from pq_open
                #s.t. f(idx_n_best) is smallest in pq_open
            #.pop() gives (key,value)
            idx_n_best, _ = pq_open.pop() #gets smallest pq_open
            # Remove idx_n_best from pq_open and append it to idx_closed
            if idx_n_best in idx_closed:
                continue
            idx_closed.append(idx_n_best)

            if idx_n_best == idx_goal:
                # plot a course from start to goal using backpointers
                x_path = Graph.path(self, idx_start, idx_goal)
                return x_path
            # Get neighbors
            # Expand the list
            for idx_x in self.get_expand_list(idx_n_best, idx_closed):
                pq_open = self.expand_element(idx_n_best, idx_x, idx_goal,
                                              pq_open)
        # If pq_opens runs out of options, then no path exists
        self.idx_closed = idx_closed
        x_path = np.zeros((2, 0))
        return x_path