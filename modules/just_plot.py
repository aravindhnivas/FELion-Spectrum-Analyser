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
from FELion_definitions import colors, ShowInfo

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

def theory_exp(filelists, exp, location, save, show, dpi):

        os.chdir(location)

        plt.figure(dpi = dpi)
        e = np.genfromtxt(exp)
        xe, ye = e[:,0], e[:,1]
        exp = exp.split('\\')[-1].split('.')[0]
        plt.plot(xe,ye, 'k', alpha = 0.5, label=f'Exp:{exp}.felix')

        for n ,i in enumerate(filelists):
                t = np.genfromtxt(i)
                xt, yt = t[:,0], t[:,1]
                yt = (yt/yt.max())*ye.max()
                plt.vlines(xt, ymin=0, ymax=yt, color = colors[n], lw = 5, label = i.split('/')[-1].split('.')[0])
        
        plt.legend()
        plt.grid(True)
        plt.title('Theory vs Experiment')
        plt.xlabel('Wavenumber $cm^{-1}$')
        plt.ylabel('Normalised Intensity \n(Theory Inten. is norm. to Exp.)')
        plt.xlim(xmax = xe.max()+50, xmin = xe.min()-50)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if save: plt.savefig('theory-exp_%s.png'%exp)
        if show: plt.show()
        plt.close()

def power_plot(powerfiles, location, save, show, dpi):

        os.chdir(location)
        plt.figure(dpi = dpi)
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
                plt.plot(power_file[:,0], power_file[:,1], 'ok',ms=7)
                plt.plot(x, power_extrapolated, '-', label=powerfile+':'+str(shots))
        
        plt.legend()
        plt.grid(True)
        plt.title('Power change during scan')
        plt.ylabel('Power (mJ)')
        plt.xlabel('Wavenumber $cm^{-1}$')

        if show: plt.show()
        if save: plt.savefig('power_combined.png')
        plt.close()

def plot(filelist, location, save, show, dpi, vline, parent):
        
        os.chdir(location)

        root = Toplevel(master = parent)
        root.wm_title("Plot")

        ################################ PLOTTING DETAILS ########################################

        fig = Figure(figsize=(15, 5), dpi = dpi)
        ax = fig.add_subplot(111)

        n = 0
        for i in filelist:   
                data = np.genfromtxt(i)
                x, y = data[:,0], data[:,1]
                if not vline: ax.plot(x, y, label = i)
                else: ax.vlines(x, ymin=0, ymax=y, color = colors[n], lw = 2, label = i)
                print(f'Color-->{colors[n]}\n')
                n += 1

        ax.legend()
        ax.set_xlabel("Wavenumber(cm-1)")
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
        name.set('plot')
        filename.pack(side = 'left')

        button = ttk.Button(frame, text = 'Save', command = lambda: save_func(name.get(), location, fig))
        button.pack(side = 'left', padx = 15, ipadx = 10, ipady = 5)

        root.mainloop()

def smooth_avg(filelist, location, save, show, dpi, original_show, scale, smooth, parent):
        
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
        if len(dat)>1:
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

        #root.mainloop()