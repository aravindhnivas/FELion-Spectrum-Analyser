#!/usr/bin/python3

# DATA analysis modules
from scipy.interpolate import interp1d
import numpy as np

# Tkinter Modules
from tkinter import Toplevel

# FELion Module
from FELion_definitions import move, FELion_Toplevel

# Built-In Module
import os
from os.path import dirname, isdir, isfile, join

# Matplotlib modules
from matplotlib.lines import Line2D

class Create_Baseline():

    def __init__(self, felixfile, location, dpi, parent):

        self.parent = parent
        self.dpi = dpi

        self.felixfile = felixfile
        self.fname = felixfile.split('.')[0]
        self.basefile = f'{self.fname}.base'

        self.baseline = None
        self.data = None
        
        back_dir = dirname(location)
        folders = ["DATA", "EXPORT", "OUT"]
        if set(folders).issubset(os.listdir(back_dir)): 
            self.location = back_dir
        else: 
            self.location = location
   
        os.chdir(self.location)
        for dirs in folders: 
            if not isdir(dirs): os.mkdir(dirs)
            if isfile(self.felixfile): move(self.location, self.felixfile)
            if isfile(self.basefile): move(self.location, self.basefile)

    def felix_read_file(self):

        file = np.genfromtxt(f'DATA/{self.felixfile}')
        wn, count, sa = file[:,0], file[:,2], file[:,3]
        data = wn, count, sa
        data = np.take(data, data[0].argsort(), 1)
        self.data = data
    
    def ReadBase(self):

        file = np.genfromtxt(f'DATA/{self.basefile}')
        self.xs, self.ys = file[:,0], file[:,1]
        with open(f'DATA/{self.basefile}', 'r') as f:
            self.interpol = f.readlines()[1].strip().split('=')[-1]
    
    def SaveBase(self):

        b = np.asarray(self.baseline)
        with open(f'DATA/{self.basefile}', 'w') as f:
            f.write(f'#Baseline generated for {self.fname}.felix data file!\n')
            f.write("#BTYPE=cubic\n")
            for i in range(len(b[0])):
                f.write("{:8.3f}\t{:8.2f}\n".format(b[0][i], b[1][i]))
    
    def GuessBaseLine(self, PPS, NUM_POINTS):
        max_n = len(self.data[0]) - PPS
        Bx, By = [self.data[0][0]-0.1], [self.data[1][0]]

        for i in range(0, max_n, int(max_n/NUM_POINTS)):
            x = self.data[0][i:i+PPS].mean()
            y = self.data[1][i:i+PPS].mean()
            Bx.append(x)
            By.append(y)
        Bx.append(self.data[0][-1]+0.1)
        By.append(self.data[1][-1])

        self.xs, self.ys = Bx, By


def baseline_correction(felixfile, location, dpi, parent):
    
    base = Create_Baseline(felixfile, location, dpi, parent)

    print(f'\nLocation: {base.location}\nFilename: {base.felixfile}')

    base.felix_read_file() # read felix file
    if isfile(f'DATA/{base.basefile}'): base.ReadBase() # Read baseline file if exist else guess it
    else: base.GuessBaseLine(PPS = 5, NUM_POINTS = 10)

    ####################################### Tkinter figure #######################################
    title_name = 'Baseline Correction'
    root = Toplevel(base.parent)
    tk_widget = FELion_Toplevel(root, title_name, base.location)

    base.fig, base.canvas = tk_widget.figure(base.dpi)
    base.ax = base.fig.add_subplot(111)

    ################################ PLOTTING DETAILS ########################################
    base.ax.plot(base.data[0], base.data[1], ls='', marker='o', ms=5, markeredgecolor='r', c='r')

    base.ax.set_title('BASELINE points are drag-able!')
    base.ax.set_xlim((base.data[0][0]-70, base.data[0][-1]+70))
    base.ax.set_xlabel("wavenumber (cm-1)")
    base.ax.set_ylabel("Counts")

    ####################################### END Plotting details #####################################
    base.canvas.draw()
    ####################################### END Tkinter figure #######################################