"""
Test functions for HW1
"""

import matplotlib.pyplot as plt
import numpy as np

import me570_geometry as geometry


def segment_collision_test():
    """
    The function creates a segment from  [0;0] to
    [1;1] and a second random segment with endpoints
    contained in the square [0,1] [0,1]. It plots the two segments in green
    if they do not intersect, and in red otherwise.
    """

    vertices_a = np.array([[0, 1], [0, 1]])
    vertices_b = np.random.rand(2, 2)
    #Calls segment_collision in geometry.py
    flag_collision = geometry.segment_collision(vertices_a, vertices_b)
    if flag_collision:
        style = 'r'
    else:
        style = 'g'
        style = style + '-o'
    print(vertices_b)
    plt.plot(vertices_a[0, :], vertices_a[1, :], style)
    plt.plot(vertices_b[0, :], vertices_b[1, :], style)


def polygon_is_collision_test():
    """
    Defines a triangle, samples 50 random points in [0,1]x[0,1],
    and plots each point red (collision) or green (no collision).
    Repeat after flipping the polygon.
    """

    polygon = geometry.Polygon(np.random.uniform(0.0, 1.0, size=(2, 3)))
    points = np.random.uniform(0, 1, size=(2, 50))
    nb_points = points.shape[1]

    _, axes = plt.subplots(1, 2, figsize=(10, 5))

    for ax in axes:
        inside = []  # collision
        outside = []  # no collision

        for idx_point in range(nb_points):
            point = points[:, [idx_point]]
            if polygon.is_collision(point):
                inside.append(point)
            else:
                outside.append(point)

        plt.sca(ax)
        polygon.plot('k')

        if len(inside) > 0:
            inside = np.hstack(inside)
            plt.scatter(inside[0, :], inside[1, :], color="red", marker='o')

        if len(outside) > 0:
            outside = np.hstack(outside)
            plt.scatter(outside[0, :],
                        outside[1, :],
                        color="green",
                        marker='o')

        polygon.flip()
