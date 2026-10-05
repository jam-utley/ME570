'''
Model a sample environment for graph search with the two-link manipulator
'''

from scipy import io as scio

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
    #Create grid_theta with samples arranged U~[0,2]
    grid_theta =
    #grid_eval assess angles _1,_2 from grid_theta, tests if in collision
    grid_eval =
    #Create grid_index: NaN where grid_eval=true and sequence of unique
    #numbers (from 0 onwards) when grid_eval=False
    grid_index =
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
    pass  # Substitute with your code
    return graph
