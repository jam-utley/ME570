"""
Please merge the class and function with the me570_graph.py file from previous assignments.
"""


class Graph:
    """
    Please merge these methods with the class from previous assignments.
    """

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
        Computes the heuristic   h given by the Euclidean distance between the
        nodes with indexes   idx_x and   idx_goal.
        """
        pass  # Substitute with your code
        return h_val

    def get_expand_list(self, idx_n_best, idx_closed):
        """
        Finds the neighbors of element   idx_n_best that are not in   idx_closed
        (line  it:expand in Algorithm~ alg:astar).
        """
        pass  # Substitute with your code
        return idx_expand

    def expand_element(self, idx_n_best, idx_x, idx_goal, pq_open):
        """
        This function expands the vertex with index   idx_x (which is a neighbor
        of the one with index   idx_n_best) and updates the attribute
        graph_vector and returns an updated version of   pq_open.
        """
        pass  # Substitute with your code
        return pq_open

    def path(self, idx_start, idx_goal):
        """
        This function follows the backpointers from the node with index
        idx_goal in   graph_vector to the one with index   idx_start node, and
        returns the  coordinates (not indexes) of the sequence of traversed
        elements.
        """
        pass  # Substitute with your code
        return x_path

    def search(self, idx_start, idx_goal):
        """
        Implements the  A^* algorithm, as described by the pseudo-code in
        Algorithm~ alg:astar.
        """
        pass  # Substitute with your code
        return x_path


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
