#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.interpolate import interp1d as interpolate
from FELion_definitions import colors, ShowInfo

def theory_exp(filelists, exp, location, save, show):

        os.chdir(location)

        plt.figure(dpi=100)
        e = np.genfromtxt(exp)
        xe, ye = e[:,0], e[:,1]
        exp = exp.split('\\')[-1].split('.')[0]
        plt.plot(xe,ye, 'k', alpha = 0.5, label=f'Exp:{exp}.felix')

        for n ,i in enumerate(filelists):
                t = np.genfromtxt(i, comments='F')
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

def power_plot(powerfiles, location, save,show):

        os.chdir(location)
        plt.figure()
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

def plot(filelist, location, save, show):
        
        os.chdir(location)

        for i in filelist:
                data = np.genfromtxt(i)
                x, y = data[:,0], data[:,1]
                plt.plot(x, y, label = i)

        plt.legend()
        plt.xlabel("Wavenumber(cm-1)")

        if show: plt.show()
        
        if save: 
                plt.savefig('combined.png')
                ShowInfo("SAVED:", "Filename: combined.png")

        plt.close()