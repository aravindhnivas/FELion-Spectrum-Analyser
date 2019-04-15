#!/usr/bin/python3

# DATA analysis modules
import numpy as np
from scipy.optimize import curve_fit

# Custom Modules
from timescan_plot import timescanplot

# Built-In modules
import os
from time import time as check_time

# Tkinter modules
from tkinter import Toplevel, ttk, BooleanVar

# FELion Modules
from FELion_definitions import FELion_Toplevel

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

    tk_widget.check_button_maker(masslist, x = 0.1, y = 0.5)

    ####################################### END Plotting details #######################################
    
    canvas.draw()

    ####################################### END Tkinter figure #######################################
    
    t1 = check_time()
    print(f'Kinetics Simulation completed in {(t1-t0)*100:.2f} ms\n')

