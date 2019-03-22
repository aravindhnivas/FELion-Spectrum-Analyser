#!/usr/bin/python3

## MODULES
# Data analysis and visualisation Modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.ticker import MultipleLocator

# Built-In Modules
import os
from os.path import join, isdir, isfile
import shutil

# FELion Definitions
from FELion_definitions import ShowInfo, copy, move, ErrorInfo, var_find

def massSpec(*args):

    t, ts, lgs, minor, major, majorTickSize, \
    xlabelsz, ylabelsz, fwidth, fheight, avgname,\
    location, mname, temp, ie,\
    save, combine, fname, filelist = args

    try:
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

            fig, ax = plt.subplots(figsize = (fwidth, fheight), dpi = 100)
    
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


            if save:
                ShowInfo("SAVED", f"File {fname}.png saved \nin MassSpec_DATA directory")
                plt.savefig(join(my_path, 'MassSpec_DATA', f'{fname}.png'))
                plt.show()

            else: plt.show()
            
            plt.close()

        if combine:
            if filelist == []: 
                return ErrorInfo("Select Files: ", "Click Select File(s)")

            fig1, ax1 = plt.subplots(figsize = (fwidth, fheight), dpi = 100)

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
            
            if save:
                ShowInfo("SAVED", f"File {avgname}.png saved \nin MassSpec_DATA directory")
                plt.savefig(join(my_path, 'MassSpec_DATA', f'{avgname}.png'))
                plt.show()
            else:
                plt.show()

            plt.close()

    except Exception as e:
        ErrorInfo("ERROR", e)