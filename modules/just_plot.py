#!/usr/bin/python3

# Impoerting Modules

# DATA analysis modules
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy.interpolate import interp1d as interpolate
from scipy.signal import savgol_filter as fit
from glob2 import glob

# FELion Module
from FELion_definitions import colors, ShowInfo, FELion_Toplevel

# Built-In Module
import os
from os.path import isfile

# Matplotlib Modules for tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# Embedding Matplotlib in tkinter window
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel

def save_func(name, location, fig):
        if isfile(f'{name}.png'): 
                if askokcancel('Overwrite?', f'File: {name}.png already present. \nDo you want to Overwrite the file?'): 
                        fig.savefig(f'{name}.png')
                        ShowInfo('SAVED', f'File: {name}.png saved in \n{location}\n directory')
        else: 
                fig.savefig(f'{name}.png')
                ShowInfo('SAVED', f'File: {name}.png saved in \n{location}\n directory')

def power_plot(powerfiles, location, save, show, dpi, parent):

        os.chdir(location)
        
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, 'PowerPlot', location)

        fig, canvas = tk_widget.figure((10, 5), dpi)
        ax = fig.add_subplot(111)

        ################################ PLOTTING DETAILS ########################################
        for powerfile in powerfiles:
                with open(powerfile, 'r') as f:
                        for i in f:
                                if i.find('#SHOTS')>=0:
                                        shots = int(i.strip().split('=')[-1])
                                        break

                power_file = np.genfromtxt(powerfile)
                power_file_extrapolate = interpolate(power_file[:,0], power_file[:,1], kind = 'linear', fill_value = 'extrapolate')

                temp = np.genfromtxt(powerfile.split('.')[0]+'.felix')
                x = temp[:,0]

                power_extrapolated = power_file_extrapolate(x)
                ax.plot(power_file[:,0], power_file[:,1], 'ok',ms=7)
                ax.plot(x, power_extrapolated, '-', label=powerfile+':'+str(shots))
        
        ax.legend()
        ax.grid(True)
        ax.set_title('Power change during scan')
        ax.set_ylabel('Power (mJ)')
        ax.set_xlabel('Wavenumber $cm^{-1}$')

        canvas.draw()

def plot(filelist, location, dpi, parent):
        
        os.chdir(location)

        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, 'Plot', location)

        fig, canvas = tk_widget.figure((10, 5), dpi)
        ax = fig.add_subplot(111)

        ################################ PLOTTING DETAILS ########################################
        n = 0
        for i in filelist:   
                data = np.genfromtxt(i)
                x, y = data[:,0], data[:,1]
                
                ax.plot(x, y, label = i)

        ax.legend()
        ax.set_xlabel("Wavenumber(cm-1)")
        ax.grid(True)

        canvas.draw()

def smooth_avg(filelist, location, dpi, original_show, scale, smooth, parent):
        
        os.chdir(location)
        dat = [i for i in filelist if i.find('.dat')>=0]
        tsv = [i for i in filelist if not i.find('.dat')>=0]

        window_length, polyorder = np.asarray(smooth.split(','), dtype = np.int)
        print(f'\nSavitzky-Golay filter for smoothening of data\nWindow Length --> {window_length}\nPolyorder --> {polyorder}\n')

        root = Toplevel(master = parent)
        root.wm_title("Exp-Theory")

        ################################ PLOTTING DETAILS ########################################

        fig = Figure(figsize=(15, 5), dpi = dpi)
        ax = fig.add_subplot(111)

        y_list = []
        n = 0
        if len(dat)>0:
                for i in dat:
                        if i.find('.dat')>=0:
                                data = np.genfromtxt(i)
                                x, y = data[:,0], data[:,1]
                                y = y - y.min()

                                y1 = y_fit = np.array(fit(y, window_length, polyorder)) # Apply a Savitzky-Golay filter for smoothening of data. "fit(data, window_length, polyorder)"
                                y_fit = y_fit - y_fit.min()

                                y_list.append(y_fit.max())

                                if original_show:       # To compare the original with the smoothened data
                                        ax.plot(x, y, label = f'{i}_Original')
                                        ax.plot(x, y1, label = f'{i}_fit')

                                elif len(tsv)<1 : ax.plot(x, y_fit, label = i)
                                else:  ax.plot(x, y_fit, 'k')
                
                y_list = np.array(y_list)

        n = 0
        if len(tsv)>0:
                for i in tsv:
                        data = np.genfromtxt(i)
                        x, y = data[:,0], data[:,1]

                        x = x * scale
                        if len(dat)>1: y = y/y.max()*y_list.max()

                        ax.vlines(x, ymin = 0, ymax = y, color = colors[n], lw = 2, label = i)
                        n += 1

        #ax.legend()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.7))

        ax.set_xlabel("Wavenumber(cm-1)")
        ax.set_ylabel("Nomalised")
        ax.grid(True)

        # Drawing in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master = root)
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = 1)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = 1)

        frame = Frame(root, bg = 'light grey')
        frame.pack(side = 'bottom', fill = 'both', expand = True)

        label = Label(frame, text = 'Save as:')
        label.pack(side = 'left', padx = 15, ipadx = 10, ipady = 5)

        name = StringVar()
        filename = Entry(frame, textvariable = name)
        name.set('exp_theory')
        filename.pack(side = 'left', padx = 15, ipadx = 10, ipady = 5)

        button = ttk.Button(frame, text = 'Save', command = lambda: save_func(name.get(), location, fig))
        button.pack(side = 'left', padx = 15, ipadx = 10, ipady = 5)
