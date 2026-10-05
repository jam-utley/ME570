'''
Model a sample environment for graph search with the two-link manipulator
'''

from scipy import io as scio
import numpy as np
from me570_robot import TwoLink
from me570_graph import Graph

obstacle_points = scio.loadmat('twolink_testData.mat')['obstaclePoints']


def twolink_grid_sample(nb_samples_theta):
    """
    The function should:
     -  Create an array, grid_theta, with nb_samples_theta values
    uniformly spaced in the interval [0,2 ];
     -  Iterate over angles  _1, _2 taken from   grid_theta, and tests
    whether the corresponding configuration of the two-link manipulator is
    in collision with the points in the array   obstacle_points provided in
    the file  !70!DarkSeaGreen2 me570_environment.py, storing the result in
    the Boolean array   grid_eval.
     -  Create an array   grid_index of size [nb_samples_theta x
    nb_samples_theta] that contains   NaN in the locations where   grid_eval
    is   True, and a sequence of unique sequential numbers (starting from
    zero) in the locations where   grid_eval is False.
    """
    #Create grid_theta with samples spaced uniformally
    grid_theta = np.linspace(0, 2*np.pi, nb_samples_theta)
    #grid_eval assess angles _1,_2 from grid_theta, tests if in collision
    grid_eval = np.zeros((nb_samples_theta, nb_samples_theta),dtype=bool)
    for i, theta_1 in grid_theta:
        for j, theta_2 in grid_theta:
            theta_array = np.array([[theta_1],[theta_2]])
            grid_eval[i,j] = TwoLink.is_collision(TwoLink.self, theta_array,
                                                  obstacle_points)
            #J NOTE: I feel that may need to iterate through obstacle
            #points but may handle like MATLAB so idk
    #Create grid_index: NaN where grid_eval=true and sequence of unique
    #numbers (from 0 onwards) when grid_eval=False
    grid_index = np.full(grid_eval.shape, np.nan)
    no_collision_points = ~grid_eval
    grid_index[no_collision_points] = np.arange(np.count_nonzero(
        no_collision_points))
    return grid_theta, grid_index


def twolink_grid_to_graph(grid_theta, grid_index):
    """
    The function should
     -  Call the function twolink_grid_sample to obtain the   grid_eval and
     grid_index arrays (as described in Question~q:grid_sample).
     -  Create a   graph_vector data structure (described in the
    sec:graph_vector section) according to an eight-connected neighborhood
    in the grid, where the index of each node in the list of dictionaries
    (which is also used for the   neighbors lists) is given by the contents
    of   graph_index. Edges in the graph should exist only if the
    corresponding neighboring locations in the grid are both collision-free.
    Use the norm of the difference between vectors  [smallmatrix _1\\ _2
    smallmatrix ] for the edge cost.
    """
    #pass  # Substitute with your code
    nb_samples_theta = grid_theta.shape[0]
    (grid_theta, grid_index) = twolink_grid_sample(nb_samples_theta)
    graph = np.full(grid_theta.shape, 
                    {"neighbors" : np.zeros([8,1]),
                     "neighbors_cost" : np.zeros([8,1]),
                     "g" : 0,
                     "x" : (~grid_index)}) 
                    #x is the location of the vertex in graph_index
                    #Apply mask?
    #AHHHH Need to fix this. Don't understand graph_vector...
    return graph
