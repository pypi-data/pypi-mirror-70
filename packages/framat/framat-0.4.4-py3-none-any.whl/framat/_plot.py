#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the FramAT authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Plotting
"""

from datetime import datetime
from math import ceil
from random import randint
import os

from commonlibs.math.vectors import unit_vector
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

from . import MODULE_NAME
from ._element import GlobalSystem
from ._log import logger


class PlotItems:
    beam_index = 'beam_index'
    deformed = 'deformed'
    forces = 'forces'
    global_axes = 'global_axes'
    moments = 'moments'
    node_uids = 'node_uids'
    nodes = 'nodes'
    undeformed = 'undeformed'

    @classmethod
    def to_list(cls):
        return [v for k, v in cls.__dict__.items() if not k.startswith('__')]


class C:
    BC = 'black'
    BC_TEXT = 'white'
    CONC_FORCE = 'steelblue'
    CONC_MOMENT = 'purple'
    DEFAULT = 'grey'
    DEFORMED = 'red'
    DIST_FORCE = 'steelblue'
    DIST_MOMENT = 'purple'
    FREENODE_FORCE = 'black'
    FREENODE_MOMENT = 'grey'
    FREENODE_POINT = 'navy'
    GLOBAL_SYS = 'blue'
    LOCAL_SYS = 'green'
    MASS = 'maroon'
    MASS_LOAD = 'maroon'
    UNDEFORMED = 'grey'


def plot_all(m):
    """Create all plots defined in the model object"""

    mpp = m.get('post_proc', None)
    if not mpp:
        return
    if not mpp.get('plot', ()):
        return

    ps = m.get('post_proc').get('plot_settings', {})
    abm = m.results.get('mesh').get('abm')

    num_tot = m.get('post_proc').len('plot')
    for plot_num, _ in enumerate(m.get('post_proc').iter('plot')):
        logger.info(f"Creating plot {plot_num + 1}/{num_tot}...")
        ax = init_3D_plot(*abm.get_lims())
        add_items_per_beam(m, ax, plot_num)
        add_global_axes(m, ax, plot_num)
        plt.tight_layout()

        if ps.get('save', False):
            now = datetime.now().strftime("%F_%H%M%S")
            ext = 'png'
            rand = randint(100, 999)
            fname = f"{MODULE_NAME.lower()}_{now}_{plot_num+1:02}_{rand}.{ext}"
            fname = os.path.join(os.path.abspath(ps.get('save')), fname)
            logger.info(f"Saving plot to file {fname!r}...")
            plt.savefig(fname, dpi=300, format='png')

    if ps.get('show', False):
        plt.show()

    plt.close('all')


def init_3D_plot(x_lims, y_lims, z_lims):
    """
    Inititalize the 3D plot

    Args:
        :x_lims: (tuple) min and max x-value
        :y_lims: (tuple) min and max y-value
        :z_lims: (tuple) min and max z-value
    """

    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')

    # Avoid setting same min and max value by adding diff
    diff = (-1e-6, 1e-6)
    ax.set_xlim(*(x+d for x, d in zip(x_lims, diff)))
    ax.set_ylim(*(y+d for y, d in zip(y_lims, diff)))
    ax.set_zlim(*(z+d for z, d in zip(z_lims, diff)))

    set_equal_aspect_3D(ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return ax


def set_equal_aspect_3D(ax):
    """
    Set aspect ratio of plot correctly

    Args:
        :ax: (obj) axis object
    """

    # See https://stackoverflow.com/a/19248731
    # ax.set_aspect('equal') --> raises a NotImplementedError
    # See https://github.com/matplotlib/matplotlib/issues/1077/

    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:, 1] - extents[:, 0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)


def args_plot(m, color, marker=None):
    args = {
        'linewidth': m.get('post_proc').get('plot_settings', {}).get('linewidth', 2),
        'markersize': m.get('post_proc').get('plot_settings', {}).get('markersize', 5),
        'color': color,
    }
    if marker is not None:
        args['marker'] = marker
    return args


def args_scatter(m, color, marker=None):
    args = {
        'linewidth': m.get('post_proc').get('plot_settings', {}).get('linewidth', 2),
        'color': color,
    }
    return args


def args_text(m, color):
    args = {
        'fontsize': m.get('post_proc').get('plot_settings', {}).get('fontsize', 10),
        'color': color,
        'bbox': dict(facecolor='orange', alpha=0.5),
        'horizontalalignment': 'center',
        'verticalalignment': 'bottom',
    }
    return args


def add_global_axes(m, ax, plot_num):
    to_show = m.get('post_proc').get('plot')[plot_num]

    if 'global_axes' in to_show:
        orig = GlobalSystem.Origin
        X = GlobalSystem.X
        Y = GlobalSystem.Y
        Z = GlobalSystem.Z
        ax = _coordinate_system(ax, orig, (X, Y, Z), ('X', 'Y', 'Z'), color=C.GLOBAL_SYS)


def _coordinate_system(plot, origin, axes, axes_names, color, scale=1):
    axes = [scale*np.array(axis) for axis in axes]
    x_axis, y_axis, z_axis = axes

    for axis, axis_name in zip(axes, axes_names):
        x, y, z = origin
        u, v, w = axis
        plot.scatter(x, y, z)
        plot.quiver(x, y, z, u, v, w, length=1)
        plot.text(x+u, y+v, z+w, axis_name)

    # Plot xy-plane
    p1 = np.array(origin)
    p2 = np.array(origin + y_axis)
    p3 = np.array(origin + z_axis)
    p4 = np.array(origin + y_axis + z_axis)
    points = np.array([p1, p2, p3, p4])
    xx = points[:, 0].reshape(2, 2)
    yy = points[:, 1].reshape(2, 2)
    z = points[:, 2].reshape(2, 2)
    plot.plot_surface(xx, yy, z, alpha=0.4, color=color)


def add_items_per_beam(m, ax, plot_num):
    to_show = m.get('post_proc').get('plot')[plot_num]
    abm = m.results.get('mesh').get('abm')
    marker = 'o' if 'nodes' in to_show else None

    for beam_idx in abm.beams.keys():
        xyz = abm.get_all_points(beam_idx)
        x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]

        # ----- Undeformed mesh -----
        if PlotItems.undeformed in to_show:
            ax.plot(x, y, z, **args_plot(m, C.UNDEFORMED))

        # ----- Deformed mesh -----
        if PlotItems.deformed in to_show:
            d = m.results.get('tensors').get('comp:U')
            xd = x + abm.gbv(d['ux'], beam_idx)
            yd = y + abm.gbv(d['uy'], beam_idx)
            zd = z + abm.gbv(d['uz'], beam_idx)
            ax.plot(xd, yd, zd, **args_plot(m, C.DEFORMED, marker=marker))

        # ----- Forces -----
        if PlotItems.forces in to_show:
            d = m.results.get('tensors').get('comp:F')
            Fx = abm.gbv(d['Fx'], beam_idx)
            Fy = abm.gbv(d['Fy'], beam_idx)
            Fz = abm.gbv(d['Fz'], beam_idx)
            # ax.quiver(x, y, z, Fx, Fy, Fz, color=C.CONC_FORCE)
            ax.quiver(xd, yd, zd, Fx, Fy, Fz, color=C.CONC_FORCE)

        # ----- Moments -----
        if PlotItems.moments in to_show:
            d = m.results.get('tensors').get('comp:F')
            Fx = abm.gbv(d['Mx'], beam_idx)
            Fy = abm.gbv(d['My'], beam_idx)
            Fz = abm.gbv(d['Mz'], beam_idx)
            # ax.quiver(x, y, z, Fx, Fy, Fz, color=C.CONC_FORCE)
            ax.quiver(xd, yd, zd, Fx, Fy, Fz, color=C.CONC_FORCE)

        # ----- Beam index -----
        if PlotItems.beam_index in to_show:
            center = ceil(len(x)/2)
            coord = (x[center], y[center], z[center])
            ax.text(*coord, str(beam_idx), **args_text(m, color=C.BC))

        # ----- Named nodes -----
        if PlotItems.node_uids in to_show:
            for uid, coord in abm.named_nodes[beam_idx].items():
                ax.text(*coord, uid, **args_text(m, color=C.BC))
