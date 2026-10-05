"""
segment_collision_v3.py

Copy of the version Hugh pasted for verification (tol-based rewrite of all five
endpoint-overlap conditions; conditions 4 and 5 simplified per the prior turn's
advice, conditions 2 and 3 left with the redundant "other pair is far apart" tail).
NOTE: import lines below were not in the original pasted snippet; added so this
file is runnable/self-contained.
"""
import math
import numpy as np


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

    #Seperate vertices_a and vertices_b into points
    #vertices_a_start = vertices_a[:,0]
    #vertices_a_end   = vertices_a[:,1]
    #vertices_b_start = vertices_b[:,0]
    #vertices_b_end   = vertices_b[:,1]

    #check length of line segments
    vertices_a_len = math.sqrt((vertices_a[0,0]-vertices_a[0,1])**2 + (vertices_a[1,0]- vertices_a[1,1])**2)
    vertices_b_len = math.sqrt((vertices_b[0,0]-vertices_b[0,1])**2 + (vertices_b[1,0]- vertices_b[1,1])**2)
    if vertices_a_len < tol or vertices_b_len < tol:
        return False

    #check overlap of both endpoints, then overlap of just a single endpoint
    #if vertices_a_start == vertices_b_end and vertices_b_start == vertices_a_end:
    #    flag = True #True because they completely overlap
    
    #if vertices_a[0,0]==vertices_b[0,1] and vertices_a[1,0]==vertices_b[1,1] and vertices_a[0,1]==vertices_b[0,0] and vertices_a[1,1]==vertices_b[1,0]:
    #    return False
    #elif vertices_a[0,0]==vertices_b[0,1] and vertices_a[1,0]==vertices_b[1,1] and vertices_a[0,1]!=vertices_b[0,0] and vertices_a[1,1]!=vertices_b[1,0]:
    #    return False
    #elif vertices_a[0,0]!=vertices_b[0,1] and vertices_a[1,0]!=vertices_b[1,1] and vertices_a[0,1]==vertices_b[0,0] and vertices_a[1,1]==vertices_b[1,0]:
    #    return False
    #elif vertices_a[0,0]==vertices_b[0,0] and vertices_a[1,0]==vertices_b[1,0]:# and vertices_a[0,1]!=vertices_b[0,1] and vertices_a[1,1]!=vertices_b[1,1]:
    #    return False
    #elif vertices_a[0,1]==vertices_b[0,1] and vertices_a[1,1]==vertices_b[1,1]:# and vertices_a[0,1]==vertices_b[0,1] and vertices_a[1,1]==vertices_b[1,1]:
    #    return False
    
    if (abs(vertices_a[0,0]-vertices_b[0,1]) < tol and abs(vertices_a[1,0]-vertices_b[1,1]) < tol and abs(vertices_a[0,1]-vertices_b[0,0]) < tol and abs(vertices_a[1,1]-vertices_b[1,0]) < tol):
        return False
    elif (abs(vertices_a[0,0]-vertices_b[0,1]) < tol and abs(vertices_a[1,0]-vertices_b[1,1]) < tol and abs(vertices_a[0,1]-vertices_b[0,0]) > tol and abs(vertices_a[1,1]-vertices_b[1,0]) > tol):
        return False
    elif (abs(vertices_a[0,0]-vertices_b[0,1]) > tol and abs(vertices_a[1,0]-vertices_b[1,1]) > tol and abs(vertices_a[0,1]-vertices_b[0,0]) < tol and abs(vertices_a[1,1]-vertices_b[1,0]) < tol):
        return False
    elif (abs(vertices_a[0,0]-vertices_b[0,0]) < tol and abs(vertices_a[1,0]-vertices_b[1,0]) < tol):
        return False
    elif (abs(vertices_a[0,1]-vertices_b[0,1]) < tol and abs(vertices_a[1,1]-vertices_b[1,1]) < tol):
        return False

    #if vertices_a_start == vertices_b_end or vertices_b_start == vertices_a_end:
    #    flag = False

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
        return True    
        #flag = True
    else:  #If they are colinear or do not intersect, it returns False
        #flag = False
        return False

    #return flag
