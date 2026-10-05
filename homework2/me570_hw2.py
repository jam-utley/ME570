"""
Functions to test algorithms and create plots
"""

import matplotlib.pyplot as plt
import numpy as np

from me570_environment import obstacle_points
from me570_robot import TwoLink


def twolink_plot_collision_test():
    """
    This function generates 30 random configurations  loads the  points variable from the file !70 DarkSeaGreen2 twolink_testData mat (provided with the homework , and then display the results using  twolink_plotCollision to plot the manipulator in red if it is in collision  and green otherwise
    """
    nb_configurations = 3
    two_link = TwoLink()
    theta_random = 2 * np.pi * np.random.rand(2, nb_configurations)
    plt.plot(obstacle_points[0, :], obstacle_points[1, :], 'r*')
    for i_theta in range(0, nb_configurations):
        theta = theta_random[:, i_theta:i_theta + 1]
        two_link.plot_collision(theta, obstacle_points)

    plt.show()
