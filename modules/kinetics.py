#!/usr/bin/python3

# DATA analysis modules
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import unumpy as unp

# Custom Modules
from timescan_plot import timescanplot

# Built-In modules
import os
from time import time as check_time

# Tkinter modules
from tkinter import Toplevel, ttk, BooleanVar

# FELion Modules
from FELion_definitions import FELion_Toplevel, FELion_widgets

####################################### Modules Imported #######################################

def kinetics(scanfile, location, dpi, parent):

    t0 = check_time()
    ####################################### Initialisation #######################################

    os.chdir(location)
    time, counts, masslist, iterations, res, b0 = timescanplot(scanfile, location, dpi, parent, kinetics = True)
    
    ####################################### END Initialisation #######################################

    ####################################### Tkinter figure #######################################

    ## Embedding figure to tkinter Toplevel
    title_name = f'Kinetics: {scanfile}'
    root = Toplevel(parent)

    tk_widget = FELion_Toplevel(root, title_name, location)

    fig, canvas = tk_widget.figure(dpi, figsize=(15,5))
    ax = fig.add_subplot(111)

    frame = tk_widget.get_widget_frame()
    widget = FELion_widgets(frame)

    log = widget.entries('Check', 'Log', 0.1, 0.3, relwidth = 0.5, relheight = 0.05, default = False)

    widget.labels('H2: ', 0.1, 0.4, relwidth = 0.2, relheight = 0.05, bd = 2)
    reactant = widget.entries('Entry', '# density', 0.4, 0.4, relwidth = 0.4, relheight = 0.05, bd = 5)

    widget.labels('He: ', 0.1, 0.5, relwidth = 0.2, relheight = 0.05, bd = 2)
    He = widget.entries('Entry', '# density', 0.4, 0.5, relwidth = 0.4, relheight = 0.05, bd = 5)
    
    eq = widget.entries('Entry', 'Equations', 0.1, 0.6, relwidth = 0.7, relheight = 0.05, bd = 5)
    tk_widget.check_button_maker(masslist, x = 0.1, y = 0.8)

    ####################################### PLOTTING DETAILS #######################################

    def plot():
        
        mass_check = tk_widget.get_check_values()

        temp_mean, temp_error = [], []
        counter = 0
        for n, i in zip(iterations, masslist):

            if mass_check[i].get():
                print(f'Plotting Mass: {i}\n')
                lg = f'{i}[{n}]; B0: {b0}ms; Res: {res}'
                ax.errorbar(time, counts[f'm{i}'], counts[f'me{i}'], fmt='.-', label = lg)

                temp_mean.append(counts[f'm{i}'])
                temp_error.append(counts[f'me{i}'])

                counter += 1
            
        temp_mean_with_error = unp.uarray(temp_mean, temp_error)
        temp_sum_mean_with_error = temp_mean_with_error.sum(axis = 0)

        if counter>1: 
            ax.errorbar(time, unp.nominal_values(temp_sum_mean_with_error), unp.std_devs(temp_sum_mean_with_error), fmt = '--', label = f'SUM TOTAL', color = 'k')
        
        if log.get(): 
            ax.set_yscale('log')

        # figure details      
        ax.set_title('Time Scan plot for %s'%scanfile)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Counts')
        ax.legend()
        ax.grid(True)

    def update():

        t0 = check_time()
        ax.clear()

        plot()
        canvas.draw()

        t1 = check_time()

        print(f'Redrawn in {(t1-t0)*100:.2f} ms')

    plot()

    widget.buttons('Update', 0.1, 0.7, update, relwidth = 0.5, relheight = 0.05)

    ####################################### END Plotting details #######################################
    canvas.draw()
    ####################################### END Tkinter figure #######################################
    
    t1 = check_time()
    print(f'Kinetics Simulation completed in {(t1-t0)*100:.2f} ms\n')