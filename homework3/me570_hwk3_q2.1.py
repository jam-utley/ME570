#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 10:27:11 2026

Code for ME570 Hwk 3 Q 2.1 report

@author: james-utley
"""
import numpy as np
from scipy import io as scio
from matplotlib import pyplot as plt
from me570_robot import TwoLink, TwoLinkGraph
import pickle

class NumpyCompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module.startswith('numpy._core'):
            module = module.replace('numpy._core', 'numpy.core', 1)
        return super().find_class(module, name)

obstacle_points = scio.loadmat('twolink_testData.mat')['obstaclePoints']
print(obstacle_points.shape)

#EASY

theta_start = np.array([[0.76], [0.12]])   # values from the assignment
theta_goal = np.array([[0.76], [6.00]])


two_link_graph = TwoLinkGraph()
with open('twolink_graph_free_space.pkl', 'rb') as fid:
    two_link_graph.graph = NumpyCompatUnpickler(fid).load()

theta_path = two_link_graph.search_start_goal(theta_start, theta_goal)

plt.figure()
plt.plot(obstacle_points[0, :], obstacle_points[1, :], 'k*')
plt.gca().set_aspect('equal')
plt.xlabel('x')
plt.ylabel('y')
plt.title('obstacle_points, easy start stop')
TwoLink().plot_animate(theta_path, fps=10)
plt.show()

plt.figure()
two_link_graph.graph.plot(flag_edges=False, flag_backpointers_cost=False)
plt.plot(theta_path[0, :], theta_path[1, :], 'r-', linewidth=2)
plt.plot(theta_start[0], theta_start[1], 'go')
plt.plot(theta_goal[0], theta_goal[1], 'ms')
plt.xlabel(r'$\theta_1$ (rad)')
plt.ylabel(r'$\theta_2$ (rad)')
plt.gca().set_aspect('equal')
plt.savefig('twolink_cspace_path.png', dpi=150)

#MEDIUM

theta_start = np.array([[0.76], [0.12]])   # values from the assignment
theta_goal = np.array([[0.76], [2.72]])


two_link_graph = TwoLinkGraph()
with open('twolink_graph_free_space.pkl', 'rb') as fid:
    two_link_graph.graph = NumpyCompatUnpickler(fid).load()

theta_path = two_link_graph.search_start_goal(theta_start, theta_goal)

plt.figure()
plt.plot(obstacle_points[0, :], obstacle_points[1, :], 'k*')
plt.gca().set_aspect('equal')
plt.xlabel('x')
plt.ylabel('y')
plt.title('obstacle_points, medium start stop')
TwoLink().plot_animate(theta_path, fps=10)
plt.show()

plt.figure()
two_link_graph.graph.plot(flag_edges=False, flag_backpointers_cost=False)
plt.plot(theta_path[0, :], theta_path[1, :], 'r-', linewidth=2)
plt.plot(theta_start[0], theta_start[1], 'go')
plt.plot(theta_goal[0], theta_goal[1], 'ms')
plt.xlabel(r'$\theta_1$ (rad)')
plt.ylabel(r'$\theta_2$ (rad)')
plt.gca().set_aspect('equal')
plt.savefig('twolink_cspace_path.png', dpi=150)