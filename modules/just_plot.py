#!/usr/bin/python3

# Impoerting Modules

# DATA analysis modules
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d as interpolate
from scipy.signal import savgol_filter as fit
from glob2 import glob

# FELion Module
from FELion_definitions import colors, ShowInfo

# Built-In Module
import os


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

def plot(filelist, location, save, show, dpi, vline):
        
        os.chdir(location)

        fig, ax = plt.subplots(dpi = dpi)
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

        if show: plt.show()
        
        if save: 
                plt.savefig('combined.png')
                ShowInfo("SAVED:", "Filename: combined.png")

        plt.close()

def smooth_avg(filelist, location, save, show, dpi, original_show):
        
        os.chdir(location)
        dat = [i for i in filelist if i.find('.dat')>=0]
        tsv = [i for i in filelist if not i.find('.dat')>=0]

        fig, ax = plt.subplots(dpi = dpi)

        y_list = []
        n = 0
        for i in dat:
                if i.find('.dat')>=0:
                        data = np.genfromtxt(i)
                        x, y = data[:,0], data[:,1]
                        
                        y_fit = np.array(fit(y, 21, 3))
                        y_list.append(y_fit.max())
                        if original_show: 
                                ax.plot(x, y, label = f'{i}_Original')
                                ax.plot(x, y_fit, label = f'{i}_fit')
                        else: ax.plot(x, y_fit, 'k' , label = f'{i}')
        
        y_list = np.array(y_list)

        n = 0
        for i in tsv:
                data = np.genfromtxt(i)
                x, y = data[:,0], data[:,1]
                print(f'Y:{y.shape}')
                y = y/y.max()*y_list.max()
                ax.vlines(x, ymin = 0, ymax = y, color = colors[n], lw = 2, label = i)
                n += 1

        #ax.legend()
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        ax.set_xlabel("Wavenumber(cm-1)")
        ax.set_ylabel("Nomalised")
        ax.grid(True)

        if show: plt.show()
        
        if save: 
                plt.savefig('combined.png')
                ShowInfo("SAVED:", "Filename: combined.png")

        plt.close()