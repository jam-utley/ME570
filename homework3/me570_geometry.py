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
    function should always return False.
    """
    #Information for the math was taken from this YouTube Link:
    #https://www.youtube.com/watch?v=IwKkiaoqwTc
    #Adapted from code for C, presented in this YouTube video:
    #https://www.youtube.com/watch?v=PXvNVfnUuVc&t=204s

    # tolerance to check for coincident points
    tol = 2.22e-16

    #check length of line segments
    vertices_a_len = math.sqrt((vertices_a[0,0]-vertices_a[0,1])**2 +
                               (vertices_a[1,0]- vertices_a[1,1])**2)
    vertices_b_len = math.sqrt((vertices_b[0,0]-vertices_b[0,1])**2 +
                               (vertices_b[1,0]- vertices_b[1,1])**2)
    if vertices_a_len < tol or vertices_b_len < tol:
        return False

    #Assesses the end points of the vertices for overlap within tolerance
    #If they overlap exactly
    if (abs(vertices_a[0,0]-vertices_b[0,1]) < tol
        and abs(vertices_a[1,0]-vertices_b[1,1]) < tol
        and abs(vertices_a[0,1]-vertices_b[0,0]) < tol
        and abs(vertices_a[1,1]-vertices_b[1,0]) < tol):
        return False
    #If the starting vertex of A overlaps with end of B
    elif (abs(vertices_a[0,0]-vertices_b[0,1]) < tol
          and abs(vertices_a[1,0]-vertices_b[1,1]) < tol):
        return False
    #If the end of A overlaps with the start of B
    elif (abs(vertices_a[0,1]-vertices_b[0,0]) < tol
          and abs(vertices_a[1,1]-vertices_b[1,0]) < tol):
        return False
    #If A and B share a starting point
    elif (abs(vertices_a[0,0]-vertices_b[0,0]) < tol
          and abs(vertices_a[1,0]-vertices_b[1,0]) < tol):
        return False
    #If A and B share an endpoint
    elif (abs(vertices_a[0,1]-vertices_b[0,1]) < tol
          and abs(vertices_a[1,1]-vertices_b[1,1]) < tol):
        return False

    #Check orientation of lines
    x1 = vertices_a[0,0]
    x2 = vertices_a[0,1]
    x3 = vertices_b[0,0]
    x4 = vertices_b[0,1]
    y1 = vertices_a[1,0]
    y2 = vertices_a[1,1]
    y3 = vertices_b[1,0]
    y4 = vertices_b[1,1]
    #np.sign assesses orientation (clockwise, counter clockwise, colinear)
    orientation_1 = np.sign((y2-y1)*(x3-x2)-(y3-y2)*(x2-x1)) #a,b,c
    orientation_2 = np.sign((y2-y1)*(x4-x2)-(y4-y2)*(x2-x1)) #a,b,d
    orientation_3 = np.sign((y4-y3)*(x1-x4)-(y1-y4)*(x4-x3)) #c,d,a
    orientation_4 = np.sign((y4-y3)*(x2-x4)-(y2-y4)*(x4-x3)) #c,d,b
    #If this is true, they must intersect
    if orientation_1 != orientation_2 and orientation_3 != orientation_4:
        return True
    else:  #If they are colinear or do not intersect, it returns False
        return False

    #return flag


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
        #Get the vertices
        X = self.vertices[0,:]
        Y = self.vertices[1,:]
        #For ease of computation,
        #calculate this only once since it's used multiple places
        range_x = len(X)
        #U,V store the arrow directions
        U=np.zeros(range_x)
        V=np.zeros(range_x)
        #Calculate U,V from one vertex to the next

        for i in range(0,range_x):
            #Modular division to ensure arrows point in the correct direction.
            j = (i+1)%range_x
            U[i] = X[j]-X[i]
            V[i] = Y[j]-Y[i]
        plt.quiver(X, Y, U, V, angles = 'xy', scale_units='xy',
                   scale=1,color=style)
        #X,Y are direction for arrow locations, U,V define arrow directions


    def is_filled(self):
        """
        Check whether a the polygon is filled or not by looking at the ordering
        of the vertices.
        """
        #For tracking the overall orientation
        angle_total = 0
        #For every one of the vertices,assess the angle
        #between each to determine if it is going clockwise or counterclockwise
        #gets the length of the first row, i.e. how many vertices there are
        vertex_num = len(self.vertices[0])
        for i in range(0,vertex_num):
            j=(i+1)%vertex_num #loops through vertices sequentially
            prev_i = (i-1)%vertex_num #The previous vertex to i
            angle = segment_angle(self.vertices[:,i:i+1],
                                  self.vertices[:,prev_i:prev_i+1],
                                  self.vertices[:,j:j+1], 'signed')
            angle_total += angle

        #Assesses if the angle is counter clockwise and postitive (filled)
        #or clockwise and negative
        if angle_total < 0:
            return True #i.e. filled
        else:
            return False #i.e. not filled

        #return flag

    def is_collision(self, point):
        """
        Check whether a point is in collision with the polygon. The method
        should compute the result using the winding number method. In
        particular, compute the signed angle between each pair of consecutive
        polygon vertices as seen from the query point, using the function
        segment_angle from the first part of the assignment, and sum these
        angles around the polygon.
        """

        tol = 0.00001 #orders of magnitude above expected floating-point noise

        #Compares all of the vertices to the point in question
        #angle = segment_angle(self.vertices,point)

        #gets the length of the first row,
        #i.e. how many vertices there are
        vertex_num = len(self.vertices[0])

        angle_total = 0.0

        for i in range(vertex_num):
            j = (i+1)%vertex_num
            #gives vertex0 the correct shape
            vertex0 = point.reshape(2,1)
            #gives vertex 1 and 2 the correct shape
            vertex1 = self.vertices[:,i:i+1]
            vertex2 = self.vertices[:,j:j+1]
            if (abs(vertex0[0,0]-vertex1[0,0]) < tol
                and abs(vertex0[1,0]-vertex1[1,0]) < tol):
                return False
            if (abs(vertex0[0,0]-vertex2[0,0]) < tol
                and abs(vertex0[1,0]-vertex2[1,0]) < tol):
                return False
            angle = segment_angle(vertex0, vertex1, vertex2, 'signed')
            #Check for colinearity of points
            #I chose 1e13 because  Claude found that the difference was around
            #4.6e-13, so I chose 1e-13 as a suitable tolerance
            if abs(abs(angle)-math.pi) < tol:
                return False
                #if this is True, it returns True for a collision
            #check for NaN and not allowing them to corrupt the total
            if math.isnan(angle):
                angle_total = angle_total
            else:
                angle_total += angle

        filled_or_hollow = self.is_filled()
        if filled_or_hollow == True: #i.e. Filled
            #assesses if point is within the polygon
            if abs(angle_total) > tol:
                return True #i.e. COLLISION
            else:
                return False
        else:
            if abs(angle_total) > tol:
                return False #i.e. no COLLISION
            else:
                return True

def rot2d(theta):
    """
    Create a 2-D rotation matrix from the angle  theta according to (1).
    """
    rot_theta = np.array([[math.cos(theta), -math.sin(theta)],
                          [math.sin(theta), math.cos(theta)]])
    return rot_theta
