#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 22:45:09 2026

@author: james-utley
"""

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

import me570_geometry as geometry

def polygon_plot_seven_sides_plus(clockwise=None, alpha=0.5):
    """
    Plots polygons of seven or more sides as is required for ME570 
    Homework 1, Question 2.1. Randomly chooses counterclockwise (filled) or
    clockwise (hollow) unless `clockwise` is given explicitly, and shades
    the polygon's interior when filled or the surrounding region when hollow.
    """
    if clockwise is None:
        clockwise = np.random.choice([True, False])

    num_sides = np.random.randint(7, 13)  # random integer, 7 to 12 inclusive
    vertices = np.random.uniform(0.0, 1.0, size=(2, num_sides))

    # sort by angle around the centroid for a simple polygon, in CCW order
    centroid = vertices.mean(axis=1, keepdims=True)
    angles = np.arctan2(vertices[1,:] - centroid[1,0], vertices[0,:] - centroid[0,0])
    vertices = vertices[:, np.argsort(angles)]
    if clockwise:
        vertices = vertices[:, ::-1]

    polygon = geometry.Polygon(vertices)
    polygon.plot('k')

    ax = plt.gca()
    if polygon.is_filled():
        ax.fill(vertices[0,:], vertices[1,:], color='0.7', alpha=alpha)
        ax.set_xlim(-0.1, 1.1); ax.set_ylim(-0.1, 1.1)
    else:
        margin = 0.2
        xmin, xmax = vertices[0,:].min()-margin, vertices[0,:].max()+margin
        ymin, ymax = vertices[1,:].min()-margin, vertices[1,:].max()+margin
        outer = np.array([[xmin,xmax,xmax,xmin],[ymin,ymin,ymax,ymax]])  # CCW rectangle
        path_vertices = np.hstack([outer, outer[:, :1], vertices, vertices[:, :1]]).T
        codes = ([mpath.Path.MOVETO] + [mpath.Path.LINETO]*(outer.shape[1]-1) + [mpath.Path.CLOSEPOLY] +
                 [mpath.Path.MOVETO] + [mpath.Path.LINETO]*(vertices.shape[1]-1) + [mpath.Path.CLOSEPOLY])
        ax.add_patch(mpatches.PathPatch(mpath.Path(path_vertices, codes), color='0.7', linewidth=0, alpha=alpha))
        ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')