#!/usr/bin/python3

## MODULES

# Data analysis and visualisation Modules
import numpy as np

# matplotlib modules
from matplotlib.widgets import Cursor
from matplotlib.ticker import MultipleLocator

# Tkinter Modules
from tkinter import Toplevel

# Built-In Modules
import os
from os.path import join, isdir
import shutil

# FELion Definitions
from FELion_definitions import ShowInfo, ErrorInfo, var_find, FELion_Toplevel

def massSpec(*args):

    t, ts, lgs, minor, major, majorTickSize, \
    xlabelsz, ylabelsz, fwidth, fheight, avgname,\
    location, mname, temp, ie,\
    save, combine, fname, filelist, dpi, parent = args

    try:
        ####################################### Initialisation #######################################
        os.chdir(location)
        my_path = os.getcwd()

        if not isdir("MassSpec_DATA"):
            os.mkdir("MassSpec_DATA")
        if fname.find(".mass")>=0:
            fname = fname.split(".")[0]

        if not combine:
            filename = fname + ".mass"
            res, b0, trap = var_find(filename, location)

            if not os.path.isdir("MassSpec_DATA"):
                os.mkdir("MassSpec_DATA")
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
            else:
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
           
            mass = np.genfromtxt(filename)
            x, y = mass[:,0], mass[:,1]
            
            ####################################### END Initialisation #######################################

            ####################################### Tkinter figure #######################################

            ## Embedding figure to tkinter Toplevel
            title_name = 'Mass Spec Single'
            root = Toplevel(parent)
            tk_widget = FELion_Toplevel(root, title_name, location)

            fig, canvas = tk_widget.figure(dpi, figsize = (fwidth, fheight))
            ax = fig.add_subplot(111)

            ####################################### PLOTTING DETAILS #######################################
    
            ax.semilogy(x, y, label = f'{fname}: Res: {res}; B0: {b0}ms; Trap: {trap}ms')
            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            # Configuring plot
            ax.grid(True)
            ax.set_xlabel('Mass [u]', fontsize = xlabelsz)
            ax.set_ylabel(f'Ion counts /{b0} ms', fontsize = ylabelsz)
            ax.set_title(f'{fname} for {mname} at {temp}K with IE:{ie}eV')

            l = ax.legend(title = t, fontsize = lgs)
            l.get_title().set_fontsize(ts)
            ax.xaxis.set_minor_locator(MultipleLocator(minor))
            ax.xaxis.set_major_locator(MultipleLocator(major))
            ax.tick_params(axis='both', which='major', labelsize=majorTickSize)

            ####################################### END Plotting details #######################################

            canvas.draw() # drawing in the tkinter canvas: canvas drawing board
            
            ####################################### END Tkinter figure #######################################

        if combine:
            if filelist == []: 
                return ErrorInfo("Select Files: ", "Click Select File(s)")

            ####################################### Tkinter figure #######################################

            ## Embedding figure to tkinter Toplevel
            title_name1 = 'Mass Spec Combined'
            root1 = Toplevel(parent)
            tk_widget1 = FELion_Toplevel(root1, title_name1, location)

            fig1, canvas1 = tk_widget1.figure(dpi, figsize = (fwidth, fheight))
            ax1 = fig1.add_subplot(111)

            ####################################### PLOTTING DETAILS #######################################

            for file in filelist:
                res, b0, trap = var_find(file, location)

                mass = np.genfromtxt(file)
                x, y = mass[:,0], mass[:,1]

                ax1.semilogy(x, y, label = f'{file}: Res: {res}; B0: {b0}ms; Trap: {trap}ms')

            cursor = Cursor(ax1, useblit=True, color='red', linewidth=1)

            # Configuring plot
            ax1.grid(True)
            ax1.set_xlabel('Mass [u]', fontsize = xlabelsz)
            ax1.set_ylabel(f'Ion counts', fontsize = ylabelsz)
            ax1.set_title(f'{avgname}')

            l1 = ax1.legend(title = t, fontsize = lgs)
            l1.get_title().set_fontsize(ts)
            ax1.xaxis.set_minor_locator(MultipleLocator(minor))
            ax1.xaxis.set_major_locator(MultipleLocator(major))
            ax1.tick_params(axis='both', which='major', labelsize = majorTickSize)

            ####################################### END Plotting details #######################################

            canvas1.draw() # drawing in the tkinter canvas: canvas drawing board
            
            ####################################### END Tkinter figure #######################################

    except Exception as e:
        ErrorInfo("ERROR", e)