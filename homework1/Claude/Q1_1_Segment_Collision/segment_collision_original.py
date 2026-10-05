"""
segment_collision_original.py

Unmodified copy of the segment_collision() function as pasted by Hugh for review.
NOTE: the two import lines below were NOT present in the original pasted snippet;
they're added here only so this file is runnable/self-contained. The function body
itself is untouched -- no fixes applied.
"""
import math
import numpy as np


def segment_collision(vertices_a, vertices_b):
    """
    Returns   True if the two segments intersect.  Note: if the two segments
    overlap but are colinear, or if they overlap only at a single endpoint,
    they are not considered to be intersecting. In these cases, the function
    returns   False. If one of the two segments has zero length, the
    function should always return   False.
    """
    #Information for the math was taken from this YouTube Link:
    #https://www.youtube.com/watch?v=IwKkiaoqwTc
    #Adapted from code for C, presented in this YouTube video:
    #https://www.youtube.com/watch?v=PXvNVfnUuVc&t=204s

    # tolerance to check for coincident points
    tol = 2.22e-16
    
    print("THIS IS A TEST")

    #Seperate vertices_a and vertices_b into points
    vertices_a_start = vertices_a[:,0]
    vertices_a_end   = vertices_a[:,1]
    vertices_b_start = vertices_b[:,0]
    vertices_b_end   = vertices_b[:,1]

    #check length of line segments
    vertices_a_len = math.sqrt((vertices_a[0,0]-vertices_a[0,1])**2 + (vertices_a[1,0]- vertices_a[1,1])**2)
    vertices_b_len = math.sqrt((vertices_b[0,0]-vertices_b[0,1])**2 + (vertices_b[1,0]- vertices_b[1,1])**2)
    if vertices_a_len < tol or vertices_b_len < tol:
        flag = False

    #check overlap of both endpoints, then overlap of just a single endpoint
    if vertices_a_start == vertices_b_end and vertices_b_start == vertices_a_end:
        flag = True #True because they completely overlap

    if vertices_a_start == vertices_b_end or vertices_b_start == vertices_a_end:
        flag = False

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

    if orientation_1 != orientation_2 and orientation_3 != orientation_4: #If this is true, they must intersect
        flag = True
    else:  #If they are colinear or do not intersect, it returns False
        flag = False

    return flag
