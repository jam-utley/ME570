import pickle
import numpy as np
from me570_graph import Graph
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
from me570_geometry import Polygon, rot2d


def polygons_add_x_reflection(vertices):
    """
    Given a sequence of vertices  adds other vertices by reflection
    along the x axis
    """
    vertices = np.hstack([vertices, np.fliplr(np.diag([1, -1]).dot(vertices))])
    return vertices


def polygons_generate():
    """
    Generate the polygons to be used for the two link manipulator
    """
    vertices1 = np.array([[0, 5], [-1.11, -0.511]])
    vertices1 = polygons_add_x_reflection(vertices1)
    vertices2 = np.array([[0, 3.97, 4.17, 5.38, 5.61, 4.5],
                          [-0.47, -0.5, -0.75, -0.97, -0.5, -0.313]])
    vertices2 = polygons_add_x_reflection(vertices2)
    return (Polygon(vertices1), Polygon(vertices2))


polygons = polygons_generate()

class TwoLinkGraph:
    """
    A class for finding a path for the two-link manipulator among given obstacle
points using a grid discretization and  A^*.
    """

    def __init__(self):
        self.graph = Graph()

    def load_free_space_graph(self):
        """
        Loads the contents of the file twolink_graph_free_space.pkl,
        and stores it in the   TwoLinkGraph.graph attribute of the class.
        """
        with open("twolink_graph_free_space.pkl", "rb") as fid:
            self.graph = pickle.load(fid)

    def search_start_goal(self, theta_start, theta_goal):
        """
        Use the method Graph.search to search a path in the graph stored in
        graph.
        """
        #pass  # Substitute with your code
        # Question 2.1
        # Use method Graph.search to search for
        # a path in the graph stored in graph
        return theta_path


class TwoLink:
    """
    Class for creating our two-link manipulator
    """

    def kinematic_map(self, theta):
        """
        The function returns the coordinate of the end effector, plus the
        vertices of the links, all transformed according to  _1, _2.
        """
        # pass  # Substitute with your code
        # MY WORK:::
        T_B1_B2 = np.array([[5], [0]])
        #End effector position:
        B2_p = np.array([[5], [0]])
        polygon1, polygon2 = polygons
        theta1, theta2 = np.asarray(theta).flatten()
        rot_B2_to_B1 = rot2d(theta2)
        rot_B1_to_W = rot2d(theta1)
        # Perform the transform
        vertex_effector_transf = rot_B1_to_W @ (rot_B2_to_B1 @ B2_p + T_B1_B2)
        polygon1_transf = Polygon(rot_B1_to_W @ polygon1.vertices)
        polygon2_transf = Polygon(rot_B1_to_W @ (rot_B2_to_B1 @
                                                 polygon2.vertices + T_B1_B2))
        return vertex_effector_transf, polygon1_transf, polygon2_transf

    def plot(self, theta, color):
        """
        This function should use TwoLink kinematic_map from the previous
        question together with the method Polygon plot from Homework 1
        to plot the manipulator
        """
        [_, polygon1_transf, polygon2_transf] = self.kinematic_map(theta)
        polygon1_transf.plot(color)
        polygon2_transf.plot(color)

    def is_collision(self, theta, points):
        """
        For each configuration, returns   True if  any of the links of the
        manipulator collides with  any of the points, and   False otherwise.
        Use the function Polygon.is_collision to check each link.
        """
        # pass  # Substitute with your code
        # MY WORK:::
        # Fill theta with False boolean values
        flag_theta = np.full(theta.shape[1], False, dtype=bool)
        for i in range(theta.shape[1]):
            _, polygon1_transf, polygon2_transf = self.kinematic_map(
                theta[:, [i]])
            for j in range(points.shape[1]):
                point = points[:,j]
                if (polygon1_transf.is_collision(point)
                        or polygon2_transf.is_collision(point)):
                    flag_theta[i] = True
                    break

        return flag_theta

    def plot_collision(self, theta, points):
        """
        This function should:
         - Use TwoLink.is_collision for determining if each configuration is a
        collision or not.
         - Use TwoLink.plot to plot the manipulator for all configurations,
        using a red color when the manipulator is in collision, and green
        otherwise.
         - Plot the points specified by   points as black asterisks.
        """
        # pass  # Substitute with your code
        # MY WORK:::
        flag_theta = self.is_collision(theta, points)

        for i in range(theta.shape[1]):
            if flag_theta[i]:
                self.plot(theta[:,i], 'red')
            else:
                self.plot(theta[:,i], 'green')
        plt.plot(points[0], points[1], color='black', marker='*',
                 linestyle='none')

    def plot_animate(self, theta_path, fps, decimate=1):
        """
        Displays the configurations along   theta_path as an animation, using
        TwoLink.plot to draw each configuration. Pauses for  1  fps seconds
        between draw operations. The drawings accumulate on the same figure, so
        the configurations overlap and remain visible after the animation.
        """
       # pass  # Substitute with code generated by an LLM
       #---#---#---#---#
       # Question 2.1 LLM.
       # What follows is code generated by Claude Opus 5.5, effort High on
       # October 26, 2026
       #---#---#---#---#

       # Accept a (2,) vector or a (2, N) array; always work with (2, N).
        theta_path = np.asarray(theta_path, dtype=float)
        if theta_path.ndim == 1:
            theta_path = theta_path.reshape(2, 1)
        if fps <= 0:
            raise ValueError("fps must be positive")
        decimate = max(int(decimate), 1)

        # Draw every `decimate`-th configuration, but always include the
        # last one so the goal configuration is never skipped.
        n_configs = theta_path.shape[1]
        indices = list(range(0, n_configs, decimate))
        if indices[-1] != n_configs - 1:
            indices.append(n_configs - 1)

        # Equal axes so link lengths/angles are not visually distorted.
        plt.gca().set_aspect('equal', adjustable='datalim')

        # Color encodes time (dark = start, yellow = end), because all
        # frames stay on screen and would otherwise be indistinguishable.
        # to_hex gives a plain string, like 'red'/'green' in plot_collision.
        cmap = plt.get_cmap('viridis')
        n_frames = len(indices)
        for frame, idx in enumerate(indices):
            color = mcolors.to_hex(cmap(frame / max(n_frames - 1, 1)))
            # [:, [idx]] keeps the (2, 1) column shape kinematic_map expects
            self.plot(theta_path[:, [idx]], color)
            # pause() redraws the active figure, runs the GUI event loop,
            # then waits ~1/fps s before the next configuration is added.
            plt.pause(1.0 / fps)
