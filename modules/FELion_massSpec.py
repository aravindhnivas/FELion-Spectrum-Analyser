#!/usr/bin/python3

# MODULES

# Data analysis and visualisation Modules
import numpy as np

# matplotlib modules
from matplotlib.widgets import Cursor
from matplotlib.ticker import MultipleLocator
from matplotlib import style
import matplotlib.pyplot as plt

# Tkinter Modules
from tkinter import Toplevel
from tkinter.messagebox import askokcancel

# Built-In Modules
import os
from os.path import join, isdir, isfile
import shutil
from time import time as check_time
#from pathlib import Path as pt

# FELion Definitions
from FELion_definitions import ShowInfo, ErrorInfo, var_find, FELion_Toplevel, FELion_widgets

# Error traceback
import traceback


def save():
    print('Saving Plot')
    
    def save_info():
        fig.savefig(f'./OUT/{save_name.get()}.png')
        ShowInfo('SAVED', f'File: {save_name.get()}.png saved in OUT/ directory.')
        print(f'Filename saved: {save_name.get()}.png\nLocation: {location}\n')

    if not isdir('./OUT'): os.mkdir('./OUT')
    if isfile(f'./OUT/{save_name.get()}.png'):
        if askokcancel('Overwrite?', f'File: {save_name.get()}.png already present. \nDo you want to Overwrite the file?'):
            save_info()
    else:
        save_info()

def update():

    print('Updating Plot\n')
    t0 = check_time()

    def log_check():
        if log.get():
            ax.set_yscale('log')
        else:
            ax.set_yscale('linear')
            ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    log_check()

    canvas.draw()

    t1 = check_time()
    time_log = (t1-t0)*100
    print(f'Redrawn in {time_log:.2f} ms\n')

def publication():

    global fname

    os.chdir(location)
    if not isdir('./OUT'): os.mkdir('./OUT')

    t0 = check_time()
    
    print('High Resolution image rendering\n')
    
    with plt.style.context(['science']):

        plt_fig, plt_ax =  plt.subplots(dpi=300)
        plt_ax.plot(x, y, label='$%s$'%fname.replace('_', '-'))

        # Configuring plot
        plt_ax.set_xlabel('Mass [u]')
        plt_ax.set_ylabel('$Counts$')
        title = f'Res: {res}; Trap: {trap}ms; T: {temp}K; IE :{ie}eV'
        plt_ax.set_title('$%s$'%title)

        plt_ax.legend()

        plt_fig.savefig(f'./OUT/{save_name.get()}_high_res.pdf')
        plt_fig.savefig(f'./OUT/{save_name.get()}_high_res.png', dpi=300)

        if isfile(f'./OUT/{save_name.get()}_high_res.png'): 
            print(f'File saved: {save_name.get()}_high_res.png\nLocation: {location}')
        #plt.show()

        t1 = check_time()
        time_log = (t1-t0)*100

        print(f'Rendered in {time_log:.2f} ms\n')

def massSpec(*args):

    global save_name, fig, canvas, ax, log, location, high_res, x, y, ie, temp, mname, trap, b0, res, fname

    t, ts, lgs, minor, major, majorTickSize, \
        xlabelsz, ylabelsz, fwidth, fheight, avgname,\
        location, mname, temp, ie,\
        combine, fname, filelist, dpi, parent = args

    try:

        ####################################### Initialisation #######################################

        os.chdir(location)
        my_path = os.getcwd()

        if fname.find(".mass") >= 0:
            fname = fname.split(".")[0]
        else:
            return ShowInfo('No .mass file', 'Please select a .mass file.')

        if not combine:

            filename = fname + ".mass"
            res, b0, trap = var_find(filename, location)

            mass = np.genfromtxt(filename)
            x, y = mass[:, 0], mass[:, 1]

            ####################################### END Initialisation #######################################

            ####################################### Tkinter figure #######################################

            # Embedding figure to tkinter Toplevel
            title_name = f'Mass Spec: {filename}'
            root = Toplevel(parent)
            tk_widget = FELion_Toplevel(root, title_name, location, add_buttons=False)

            # Making frames
            frame = tk_widget.get_widget_frame()
            widget = FELion_widgets(frame)

            # Making figure
            fig, canvas = tk_widget.figure(dpi, figsize=(fwidth, fheight))
            ax = fig.add_subplot(111)

            # Buttons, labels, entries and checkboxes
            
            save_name = widget.entries('Entry', 'Plot', 0.1, 0.05, relwidth = 0.5, relheight = 0.05, bd = 5)
            save_btn = widget.buttons('Save', 0.1, 0.1, save, relwidth = 0.5, relheight = 0.05)

            log = widget.entries('Check', 'Log', 0.1, 0.2, relwidth = 0.5, relheight = 0.05, default = False)
            update_btn = widget.buttons('Update Plot', 0.1, 0.3, update, relwidth = 0.5, relheight = 0.05)

            high_res = widget.buttons('Publication Quality\n(HDP-LATEX)', 0.1, 0.4, publication, relwidth = 0.7, relheight = 0.07)
            warning_label = widget.labels('Rendering is very slow', 0.1, 0.5, bg='grey', relwidth = 0.9, relheight = 0.05)
                
            ####################################### PLOTTING DETAILS #######################################
            ax.semilogy(x, y, label=f'{fname}: Res: {res}; B0: {b0}ms; Trap: {trap}ms')
            ax.grid(True)
            
            # Configuring plot
            ax.set_xlabel('Mass [u]', fontsize=xlabelsz)
            ax.set_ylabel(f'Ion counts /{b0} ms', fontsize=ylabelsz)
            ax.set_title(f'{fname} for {mname} at {temp}K with IE:{ie}eV')
            l = ax.legend(title=t, fontsize=lgs)
            l.get_title().set_fontsize(ts)
            ax.xaxis.set_minor_locator(MultipleLocator(minor))
            ax.xaxis.set_major_locator(MultipleLocator(major))
            ax.tick_params(axis='both', which='major', labelsize=majorTickSize)

            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            ####################################### END Plotting details #######################################

            canvas.draw()  # drawing in the tkinter canvas: canvas drawing board

            ####################################### END Tkinter figure #######################################

        if combine:

            if filelist == []:
                return ErrorInfo("Select Files: ", "Click Select File(s)")

            ####################################### Tkinter figure #######################################

            # Embedding figure to tkinter Toplevel
            title_name1 = 'Mass Spec Combined'
            root1 = Toplevel(parent)
            tk_widget1 = FELion_Toplevel(root1, title_name1, location)

            fig1, canvas1 = tk_widget1.figure(dpi, figsize=(fwidth, fheight))
            ax1 = fig1.add_subplot(111)
            tk_widget1.add_log_btn(ax1)

            ####################################### PLOTTING DETAILS #######################################

            for file in filelist:
                res, b0, trap = var_find(file, location)

                mass = np.genfromtxt(file)
                x, y = mass[:, 0], mass[:, 1]

                ax1.semilogy(
                    x, y, label=f'{file}: Res: {res}; B0: {b0}ms; Trap: {trap}ms')

            cursor = Cursor(ax1, useblit=True, color='red', linewidth=1)

            # Configuring plot
            ax1.grid(True)
            ax1.set_xlabel('Mass [u]', fontsize=xlabelsz)
            ax1.set_ylabel(f'Ion counts', fontsize=ylabelsz)
            ax1.set_title(f'{avgname}')

            l1 = ax1.legend(title=t, fontsize=lgs)
            l1.get_title().set_fontsize(ts)
            ax1.xaxis.set_minor_locator(MultipleLocator(minor))
            ax1.xaxis.set_major_locator(MultipleLocator(major))
            ax1.tick_params(axis='both', which='major',
                            labelsize=majorTickSize)

            ####################################### END Plotting details #######################################

            canvas1.draw()  # drawing in the tkinter canvas: canvas drawing board

            ####################################### END Tkinter figure #######################################

    except:
        ErrorInfo('Error: ', traceback.format_exc())