#!/usr/bin/python3

import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy.optimize import curve_fit

from uncertainties import ufloat as uf
from uncertainties import unumpy as unp
from timescan_plot import timescanplot


class plot:
    def __init__(self, i, l, fig):
        self.i = i
        self.l = l
        self.fig = fig
    
    def plotting(self):
        ## off plotting
        self.y_off0 = N_OFF(x, K_OFF[self.i], N[self.i])
        self.g_off0, = axs.plot(x, self.y_off0, label = 'N_OFF: [{:.2f}mJ], K_OFF={:.2fP}/J, N={:.2fP}'.format(power_values[self.i+1], uK_OFF[self.i], uN[self.i]))

        # on plotting
        self.y_on0 = N_ON((x, K_OFF[self.i]), Na0[self.i], Nn0[self.i], K_ON[self.i])
        self.g_on0, = axs.plot(x, self.y_on0, label = 'N_ON: [{:.2f}mJ], K_ON={:.2fP}/J, N={:.2fP}, Na0={:.2fP}, Nn0={:.2fP}'.format(power_values[self.i], uK_ON[self.i], uNa0[self.i]+uNn0[self.i], uNa0[self.i], uNn0[self.i]))

        # deletion plot
        self.udepletion_new = 1 - uy_ON(x, uNa0[self.i], uNn0[self.i], uK_OFF[self.i], uK_ON[self.i])/uy_OFF(x, uN[self.i], uK_OFF[self.i])
        self.depletion_new, self.depletion_error_new = unp.nominal_values(self.udepletion_new), unp.std_devs(self.udepletion_new)

        self.depletion0, = depletion_plot.plot(x, self.depletion_new, '--')

        self.X = (x, K_ON[self.i])
        self.depletion_fitted = Depletion(X, A[self.i])
        self.depletion1, = depletion_plot.plot(x, self.depletion_fitted,
                                         label = 'A = {:.2fP}, K_ON = {:.2fP}/J'.format(uA[self.i], uK_ON[self.i])
                                         )

        # controlling fitting parameters
        axcolor = 'lightgoldenrodyellow'

        self.koff_g = plt.axes([self.l, 0.12, 0.2, 0.015], facecolor=axcolor) #[left, bottom, width, height]
        self.n_g = plt.axes([self.l, 0.10, 0.2, 0.015], facecolor=axcolor)

        self.kon_g = plt.axes([self.l, 0.08, 0.2, 0.015], facecolor=axcolor)
        self.na_g = plt.axes([self.l, 0.06, 0.2, 0.015], facecolor=axcolor)
        self.nn_g = plt.axes([self.l, 0.04, 0.2, 0.015], facecolor=axcolor)

        self.koff_slider = Slider(self.koff_g, '$K_{OFF}$', 0, K_OFF[self.i]+10, valinit = K_OFF[self.i])
        self.n_slider = Slider(self.n_g, 'N', 0, N[self.i]+(N[self.i]/2), valinit = N[self.i])

        self.kon_slider = Slider(self.kon_g, '$K_{ON}$', 0, K_ON[self.i]+10, valinit = K_ON[self.i])
        self.na_slider = Slider(self.na_g, '$Na_0$', 0, Na0[self.i]+(Na0[self.i]/2), valinit = Na0[self.i])
        self.nn_slider = Slider(self.nn_g, '$Nn_0$', 0, Nn0[self.i]+(Nn0[self.i]/2), valinit = Nn0[self.i])

    def update(self, val):

        self.koff = self.koff_slider.val
        self.ukoff = uf(self.koff, K_OFF_err[self.i])

        self.n = self.n_slider.val
        self.un = uf(self.n, N_err[self.i])

        self.kon = self.kon_slider.val
        self.ukon = uf(self.kon, K_ON_err[self.i])

        self.na = self.na_slider.val
        self.una = uf(self.na, Na0_err[self.i])

        self.nn = self.nn_slider.val
        self.unn = uf(self.nn, Nn0_err[self.i])

        self.yoff = N_OFF(x, self.koff, self.n)
        self.g_off0.set_ydata(self.yoff)

        self.yon = N_ON((x, self.koff), self.na, self.nn, self.kon)
        self.g_on0.set_ydata(self.yon)

        # depletion
        self.udepletion_new1 = 1 - uy_ON(x, self.una, self.unn, self.ukoff, self.ukon)/uy_OFF(x, self.un, self.ukoff)
        self.depletion_new1, self.depletion_error_new1 = unp.nominal_values(self.udepletion_new1), unp.std_devs(self.udepletion_new1)
        self.depletion0.set_ydata(self.depletion_new1)

        self.X = (x, self.kon)
        self.pop_depletion, self.poc_depletion = curve_fit(
                Depletion, self.X , self.depletion_new1, 
                sigma = self.depletion_error_new1, 
                absolute_sigma = True
            )

        self.A_new1 = self.pop_depletion[0]
        self.perr = np.sqrt(np.diag(self.poc_depletion))[0]
        self.uA_new1 = uf(self.A_new1 , self.perr)

        self.depletion_fitted_new = Depletion(self.X, self.A_new1)
        self.depletion1.set_ydata(self.depletion_fitted_new)

        self.k = self.i*2
        legend.get_texts()[self.k].set_text('N_OFF: [{:.2f}mJ], K_OFF={:.2fP}/J, N={:.2fP}'.format(power_values[self.i+1], self.ukoff, self.un))
        legend.get_texts()[self.k+1].set_text('N_ON: [{:.2f}mJ], K_ON={:.2fP}/J, N={:.2fP}, Na0={:.2fP}, Nn0={:.2fP}'.format(power_values[self.i], self.ukon, self.una+self.unn, self.una, self.unn))
        depletion_legend.get_texts()[self.i].set_text('A = {:.2fP}, K_ON = {:.2fP}/J'.format(self.uA_new1, self.ukon))

        self.fig.canvas.draw_idle()

    self.koff_slider.on_changed(self.update)
    self.n_slider.on_changed(self.update)

    self.kon_slider.on_changed(self.update)
    self.na_slider.on_changed(self.update)
    self.nn_slider.on_changed(self.update)

    widget_position = l = 0.05
    for i in range(len(N)):

        l += 0.25