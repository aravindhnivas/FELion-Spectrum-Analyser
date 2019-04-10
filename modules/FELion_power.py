#!/usr/bin/python3

# Importing Modules

# DATA analysis modules
import numpy as np
from scipy.interpolate import interp1d

# Tkinter Modules
from tkinter import Toplevel

# FELion Module
from FELion_definitions import ErrorInfo, FELion_Toplevel

# Built-In Module
import os
from os.path import dirname

####################################### Modules Imported #######################################

class PowerCalibrator(object):
    """
    Reads the power file and provides the power and n_shot
    for any given wavenumber
    """
    def __init__(self, powerfile):
        """
        interpolation can be either 'cubic' or 'linear'
        """
        self.n_shots = 1
        self.interpol = 'linear'
        in_um = False
        xw, yw = [],[]
        with open(f'./DATA/{powerfile}') as f:
            for line in f:
                if line[0] == '#':
                    if line.find('SHOTS')==1:
                        self.n_shots = float(line.split('=')[-1])
                    if line.find('IN_UM')==1:
                        in_um = True
                    if line.find('INTERP')==1:
                        self.interpol = line.split('=')[-1].strip('\n')
                    continue
                else:
                    if not line == "\n":
                        x, y, = line.split()
                        xw.append(float(x))
                        yw.append(float(y))
        
            if in_um:
                self.xw = 10000/np.array(xw)
            else:
                self.xw = np.array(xw)

            self.yw = np.array(yw)
        
        self.f = interp1d(self.xw, self.yw, kind=self.interpol, fill_value='extrapolate')

    def power(self, x):
        return self.f(x) 

    def shots(self, x):
        if type(x)==float:
            return self.n_shots 
        else:
            return np.zeros(len(x)) + self.n_shots

    def GetCalibData(self):
        return self.xw, self.yw, self.n_shots

    def plot(self, ax, bx):
        ax.plot(self.xw, self.yw, ls='', marker='o', ms=5, markeredgecolor='r', c='r')
        ax.plot(self.xw, self.power(self.xw), ls='-', c='m')
        ax.set_ylabel("power (mJ)")
        ax.set_ylim((0, self.yw.max()*1.1))

        bx.plot(self.xw, self.shots(self.xw), ls='-', marker='o', ms=3, markeredgecolor='y', c='y')
        bx.set_ylabel("shots")

def FELion_Power(powerfile, location, dpi, parent):

    ####################################### Initialisation #######################################

    folders = ["DATA", "EXPORT", "OUT"]
    back_dir = dirname(location)
    
    if set(folders).issubset(os.listdir(back_dir)): 
        os.chdir(back_dir)
        location = back_dir
    
    else: 
        os.chdir(location)
    powerfile = powerfile.split('.')[0] + '.pow'
    ####################################### END Initialisation #######################################

    try:
        powerWN = PowerCalibrator(powerfile)
        xc, yc, n_shots = powerWN.GetCalibData()
        X = np.arange(xc.min(),xc.max(), 1)

        ####################################### Tkinter figure #######################################

        ## Embedding figure to tkinter Toplevel
        title_name = 'Power'
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi)
        ax = fig.add_subplot(111)

        ####################################### PLOTTING DETAILS #######################################
        bx = ax.twinx()
        ax.plot(xc, yc, ls='', marker='o', ms=5, markeredgecolor='r', c='r')
        bx.plot(xc, powerWN.shots(xc), ls='-', marker='o', ms=3, markeredgecolor='b', c='b')

        #plot the power calibration line:
        ax.plot(X, powerWN.power(X), ls='-', c='m')

        ax.set_title(f'Power and Number of shots in the {powerfile} file')
        ax.set_xlim((xc.min()-70, xc.max()+70))
        ax.set_ylim((0, yc.max()*1.1))
        ax.set_xlabel("wn (cm-1)")
        ax.set_ylabel("power (mJ)")
        bx.set_ylabel("n shots")

        ####################################### END Plotting details #######################################

        canvas.draw() # drawing in the tkinter canvas: canvas drawing board
        
        ####################################### END Tkinter figure #######################################
    except Exception as e:
        ErrorInfo("ERROR", e)