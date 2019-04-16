#!/usr/bin/python3

# DATA analysis modules
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import unumpy as unp
from scitools.StringFunction import StringFunction as func

# Custom Modules
from timescan_plot import timescanplot

# Built-In modules
import os
from time import time as check_time

# Tkinter modules
from tkinter import Toplevel, ttk, BooleanVar

# FELion Modules
from FELion_definitions import FELion_Toplevel, FELion_widgets, ErrorInfo, ShowInfo

####################################### Modules Imported #######################################

def kinetics(scanfile, location, dpi, parent):

    t0 = check_time()
    ####################################### Initialisation #######################################

    os.chdir(location)
    time, m, masslist, iterations, res, b0 = timescanplot(scanfile, location, dpi, parent, kinetics = True)
    
    ####################################### END Initialisation #######################################

    ####################################### Tkinter figure #######################################

    # Tkinter Toplevel
    title_name = f'Kinetics: {scanfile}'
    root = Toplevel(parent)
    tk_widget = FELion_Toplevel(root, title_name, location, add_buttons = False)

    # Making figure
    fig, canvas = tk_widget.figure(dpi, figsize=(15,5))
    ax = fig.add_subplot(111)

    # Making frames
    frame = tk_widget.get_widget_frame()
    widget = FELion_widgets(frame)

    # Buttons, labels, entries and checkboxes

    save_name = widget.entries('Entry', 'Plot', 0.1, 0.05, relwidth = 0.5, relheight = 0.05, bd = 5)
    widget.buttons('Save', 0.1, 0.1, lambda: fig.savefig(save_name.get()), relwidth = 0.5, relheight = 0.05)

    log = widget.entries('Check', 'Log', 0.1, 0.2, relwidth = 0.5, relheight = 0.05, default = False)

    widget.labels('H2: ', 0.1, 0.3, relwidth = 0.2, relheight = 0.05, bd = 2)
    H2 = widget.entries('Entry', '# density', 0.4, 0.3, relwidth = 0.4, relheight = 0.05, bd = 5)

    widget.labels('He: ', 0.1, 0.36, relwidth = 0.2, relheight = 0.05, bd = 2)
    He = widget.entries('Entry', '# density', 0.4, 0.36, relwidth = 0.4, relheight = 0.05, bd = 5)
    
    eq = widget.entries('Entry', 'Equations', 0.1, 0.45, relwidth = 0.7, relheight = 0.05, bd = 5)
    k = widget.entries('Entry', 'Rate constants', 0.1, 0.52, relwidth = 0.7, relheight = 0.05, bd = 5)

    tk_widget.check_button_maker(masslist, x = 0.1, y = 0.75)
    
    ####################################### PLOTTING DETAILS #######################################

    def plot():
        mass_check = tk_widget.get_check_values()

        temp_mean, temp_error = [], []
        counter = 0
        for n, i in zip(iterations, masslist):

            if mass_check[i].get():
                print(f'Plotting Mass: {i}\n')
                lg = f'{i}[{n}]; B0: {b0}ms; Res: {res}'
                ax.errorbar(time, m[f'{i}'], m[f'e{i}'], fmt='.-', label = lg)

                temp_mean.append(m[f'{i}'])
                temp_error.append(m[f'e{i}'])

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

    def fit():

        temp = eq.get().strip().split('=')

        fit_mass = eval(temp[0])
        var = k.get()
        fit_eq = func(f'({temp[1]})*time', independent_variable = f'time, {var}', m = m, nh = np.float(H2.get()))

        pop, popc = curve_fit(fit_eq, time, fit_mass)
        
        perr = np.sqrt(np.diag(popc))
        print(pop)

        ax.plot(time, fit_eq(time, *pop), label = 'Fit')

        '''except Exception as e:
            ShowInfo('Equation', 'Please enter the proper equation in Equation entry box.\nEg. m[18.8]=k1*m[17.8]-k2*m[19.8]\nAnd enter the rate coefficient in the next entry box (in this case, enter: k1, k2)')
            ErrorInfo('Error', e)'''

    widget.buttons('Fit', 0.1, 0.57, fit, relwidth = 0.5, relheight = 0.05)

    def update():

        t0 = check_time()
        ax.clear()

        plot()
        canvas.draw()

        t1 = check_time()

        print(f'Redrawn in {(t1-t0)*100:.2f} ms')

    plot()

    widget.buttons('Update', 0.1, 0.65, update, relwidth = 0.5, relheight = 0.05)

    ####################################### END Plotting details #######################################
    canvas.draw()
    ####################################### END Tkinter figure #######################################
    
    t1 = check_time()
    print(f'Kinetics Simulation completed in {(t1-t0)*100:.2f} ms\n')