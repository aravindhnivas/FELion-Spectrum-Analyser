#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import interp1d

class InteractivePoints(object):
    """
    Line editor
    Keys:
      'd' delete the vertex under point
      'a' insert a vertex at point
    """

    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, figure, ax, xs, ys):
        self.ax = ax
        canvas = figure.canvas

        self.line = Line2D(xs, ys, marker='s', ls='', ms=6, c='b', markeredgecolor='b', animated=True)
        self.ax.add_line(self.line)
        
        #Interpolated Line:
        self.inter_xs = np.arange(xs[0], xs[-1])
        self.funcLine = Line2D([], [], marker='', ls='-', c='b', animated=True)
        self.ax.add_line(self.funcLine)
        self.redraw_f_line()

        self._ind = None  # the active vert

        #canvas.mpl_connect('draw_event', self.draw_callback)
        #canvas.mpl_connect('button_press_event', self.button_press_callback)
        #anvas.mpl_connect('key_press_event', self.key_press_callback)
        #canvas.mpl_connect('button_release_event', self.button_release_callback)
        #canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas

    def redraw_f_line(self):
        Bx, By = self.line.get_data()
        self.inter_xs = np.arange(Bx.min(), Bx.max())

        f = interp1d(Bx, By, kind='cubic')
        self.funcLine.set_data((self.inter_xs, f(self.inter_xs))) 

fig, ax = plt.subplots()
InteractivePoints()