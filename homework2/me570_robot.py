"""
Class for a simple 2-D robot with two links
"""

import numpy as np
from matplotlib import pyplot as plt

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
