"""
Classes and functions for Polygons and Edges
"""

import math

import numpy as np
from matplotlib import pyplot as plt


def segment_angle(vertex0, vertex1, vertex2, angle_type):
    """
    Compute the angle between two edges   vertex0--  vertex1 and   vertex0--
     vertex2 that have an endpoint in common. The angle is computed by
    starting from the edge   vertex0--  vertex1, and then ``walking'' in a
    counterclockwise direction until the edge   vertex0--  vertex2 is
    reached.
    """
    # tolerance to check for coincident points
    tol = 2.22e-16

    # compute vectors corresponding to the two edges, and normalize
    vec1 = vertex1 - vertex0
    vec2 = vertex2 - vertex0

    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 < tol or norm_vec2 < tol:
        # vertex1 or vertex2 coincides with vertex0, abort
        angle = math.nan
        return angle

    vec1 = vec1 / norm_vec1
    vec2 = vec2 / norm_vec2

    # Transform vec1 and vec2 into flat 3-D vectors,
    # so that they can be used with np.inner and np.cross
    vec1flat = np.vstack([vec1, 0]).flatten()
    vec2flat = np.vstack([vec2, 0]).flatten()

    c_angle = np.inner(vec1flat, vec2flat)
    s_angle = np.inner(np.array([0, 0, 1]), np.cross(vec1flat, vec2flat))

    angle = math.atan2(s_angle, c_angle)

    angle_type = angle_type.lower()
    if angle_type == 'signed':
        # nothing to do
        pass
    elif angle_type == 'unsigned':
        angle = (angle + 2 * math.pi) % (2 * math.pi)
    else:
        raise ValueError('Invalid argument angle_type')

    return angle


def segment_collision(vertices_a, vertices_b):
    """
    Returns   True if the two segments intersect.  Note: if the two segments
    overlap but are colinear, or if they overlap only at a single endpoint,
    they are not considered to be intersecting. In these cases, the function
    returns   False. If one of the two segments has zero length, the
    function should always return   False.
    """
    pass  # Substitute with your code
    return flag


class Polygon:
    """
    Class for plotting, drawing, checking visibility, and checking collision
with polygons.
    """

    def __init__(self, vertices):
        """
        Save the input coordinates to the internal attribute   vertices.
        """
        self.vertices = vertices

    def flip(self):
        """
        Reverse the order of the vertices, i.e., transform the polygon from
        filled to hollow or from hollow to filled.
        """
        self.vertices = np.fliplr(self.vertices)

    def plot(self, style):
        """
        Plot the polygon using Matplotlib.
        """
        #For each of the vertices
        #plot the vertices
        X = self.vertices[0,:]
        Y = self.vertices[0,:]
        #Calculate U,V from one vertex to the next
        for i in range(0,len(X)):
            U[i] = self.vertices[0,i]-self.vertices[0,i-1]
            V[i] = self.vertices[1,i]-self.vertices[0,i-1]
        plt.quiver([X, Y], U, V) #X,Y are direction for arrow locations, U,V define arrow directions
#        pass  # Substitute with your code

    def is_filled(self):
        """
        Check whether a the polygon is filled or not by looking at the ordering
        of the vertices.
        """
        pass  # Substitute with your code
        return flag

    def is_collision(self, point):
        """
        Check whether a point is in collision with the polygon. The method
        should compute the result using the winding number method. In
        particular, compute the signed angle between each pair of consecutive
        polygon vertices as seen from the query point, using the function
        segment_angle from the first part of the assignment, and sum these
        angles around the polygon.
        """
        pass  # Substitute with your code
        return flag
