#!/usr/bin/python3

# Importing Modules

# DATA analysis modules
from numpy import array, genfromtxt, asarray
from scipy.interpolate import interp1d as interpolate
from scipy.signal import savgol_filter as fit

# Tkinter Modules
from tkinter import Toplevel

# FELion Module
from FELion_definitions import colors, FELion_Toplevel, ErrorInfo

# Built-In Module
import os
from os.path import isfile, dirname

# Error traceback
import traceback

####################################### Modules Imported #######################################

def power_plot(powerfile, powerfiles, combine, location, dpi, parent):

    ####################################### Initialisation #######################################

    back_dir = dirname(location)
    folders = ["DATA", "EXPORT", "OUT"]
    if set(folders).issubset(os.listdir(back_dir)):
        os.chdir(back_dir)
        location = back_dir
    else:
        os.chdir(location)

    ####################################### END Initialisation ###################################

    ####################################### Tkinter figure #######################################

    # Embedding figure to tkinter Toplevel
    title_name = 'PowerPlot'
    root = Toplevel(parent)
    tk_widget = FELion_Toplevel(root, title_name, location)

    fig, canvas = tk_widget.figure(dpi)
    ax = fig.add_subplot(111)

    ################################ PLOTTING DETAILS ########################################

    try:

        def powerplot(powerfile):
            with open(f'./DATA/{powerfile}', 'r') as f:
                for i in f:
                    if i.find('#SHOTS') >= 0:
                        shots = int(i.strip().split('=')[-1])
                        break

            power_file = genfromtxt(f'./DATA/{powerfile}')
            power_file_extrapolate = interpolate(
                power_file[:, 0], power_file[:, 1], kind='linear', fill_value='extrapolate')
            fname = powerfile.split('.')[0]

            if isfile(f'./DATA/{fname}.cfelix'):
                felixfile = f'{fname}.cfelix'
            else:
                felixfile = f'{fname}.felix'

            temp = genfromtxt(f'./DATA/{felixfile}')
            x = temp[:, 0]

            power_extrapolated = power_file_extrapolate(x)

            ax.plot(power_file[:, 0], power_file[:, 1], '.k')
            ax.plot(x, power_extrapolated, '-', label=f'{powerfile} : {shots}')

            ax.legend()
            ax.grid(True)
            ax.set_title('Power change during scan')
            ax.set_ylabel('Power (mJ)')
            ax.set_xlabel('Wavenumber $cm^{-1}$')

        if combine:
            if powerfiles == []:
                return ErrorInfo('Combine Mode active', 'Please Select some powerfiles to plot')
            for file in powerfiles:
                powerplot(file)

        else:
            if powerfile == '':
                return ErrorInfo('No File', 'Please Select a powerfile to plot')
            powerplot(powerfile)

        ####################################### END Plotting details #######################################

        canvas.draw()  # drawing in the tkinter canvas: canvas drawing board

        ####################################### END Tkinter figure #######################################
    except:
        ErrorInfo('Error: ', traceback.format_exc())


def plot(filename, filelist, combine, location, dpi, parent):

    ####################################### Initialisation #######################################

    os.chdir(location)

    ####################################### END Initialisation #######################################

    ####################################### Tkinter figure #######################################

    # Embedding figure to tkinter Toplevel
    title_name = 'Plot'
    root = Toplevel(parent)
    tk_widget = FELion_Toplevel(root, title_name, location)

    fig, canvas = tk_widget.figure(dpi)
    ax = fig.add_subplot(111)

    ####################################### PLOTTING DETAILS #######################################

    try:
        if combine:
            for i in filelist:
                data = genfromtxt(i)
                x, y = data[:, 0], data[:, 1]
                ax.plot(x, y, label=i)
        else:
            data = genfromtxt(filename)
            x, y = data[:, 0], data[:, 1]
            ax.plot(x, y, label=filename)

        ax.legend()
        ax.set_title('Plot XY')
        ax.set_xlabel("X-Axis")
        ax.set_ylabel("Y-Axis")
        ax.grid(True)

        ####################################### END Plotting details #######################################

        canvas.draw()  # drawing in the tkinter canvas: canvas drawing board

        ####################################### END Tkinter figure #######################################
    except:
        ErrorInfo('Error: ', traceback.format_exc())


def exp_theory(filelist, location, dpi, original_show, scale, smooth, parent):

    ####################################### Initialisation #######################################
    try:

        os.chdir(location)
        dat = [i for i in filelist if i.find('.dat') >= 0]
        tsv = [i for i in filelist if not i.find('.dat') >= 0]

        window_length, polyorder = asarray(smooth.split(','), dtype=int)
        print(
            f'\nSavitzky-Golay filter for smoothening of data\nWindow Length --> {window_length}\nPolyorder --> {polyorder}\n')

        ####################################### END Initialisation #######################################

        ####################################### Tkinter figure #######################################

        # Embedding figure to tkinter Toplevel
        title_name = 'Exp-Theory'
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi)
        ax = fig.add_subplot(111)

        ####################################### PLOTTING DETAILS #######################################

        y_list = []
        n = 0
        if len(dat) > 0:
            for i in dat:
                if i.find('.dat') >= 0:
                    data = genfromtxt(i)
                    x, y = data[:, 0], data[:, 1]
                    y = y - y.min()

                    # Apply a Savitzky-Golay filter for smoothening of data. "fit(data, window_length, polyorder)"
                    y1 = y_fit = array(fit(y, window_length, polyorder))
                    y_fit = y_fit - y_fit.min()

                    y_list.append(y_fit.max())

                    if original_show:       # To compare the original with the smoothened data
                        ax.plot(x, y, label=f'{i}_Original')
                        ax.plot(x, y1, label=f'{i}_fit')

                    elif len(tsv) < 1:
                        ax.plot(x, y_fit, label=i)
                    else:
                        ax.plot(x, y_fit, 'k')

            y_list = array(y_list)

        n = 0
        if len(tsv) > 0:
            for i in tsv:
                data = genfromtxt(i)
                x, y = data[:, 0], data[:, 1]

                x = x * scale
                if len(dat) > 0:
                    y = y/y.max()*y_list.max()

                ax.vlines(x, ymin=0, ymax=y, color=colors[n], lw=2, label=i)
                n += 1

        # ax.legend()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.7))
        ax.set_title('Experimental vs Theoretical')
        ax.set_xlabel("Wavenumber(cm-1)")
        ax.set_ylabel("Nomalised Intensity")
        ax.grid(True)

        ####################################### END Plotting details #######################################

        canvas.draw()  # drawing in the tkinter canvas: canvas drawing board

        ####################################### END Tkinter figure #######################################
    
    except:
        ErrorInfo('Error: ', traceback.format_exc())
