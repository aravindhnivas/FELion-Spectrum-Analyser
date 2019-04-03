#!/usr/bin/python3

## Importing Modules

# DATA Analysis modules:
import numpy as np

# Built-In modules
import os
from os.path import dirname, isdir, isfile

# FELion-Modules
from FELion_baseline import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
from FELion_definitions import ShowInfo, ErrorInfo, filecheck, move, FELion_Toplevel

# Tkinter Modules
from tkinter import Toplevel

import matplotlib.pyplot as plt

################################################################################

def export_file(fname, wn, inten):
    f = open('EXPORT/' + fname + '.dat','w')
    f.write("#DATA points as shown in lower figure of: " + fname + ".pdf file!\n")
    f.write("#wn (cm-1)       intensity\n")
    for i in range(len(wn)):
        f.write("{:8.3f}\t{:8.2f}\n".format(wn[i], inten[i]))
    f.close()

def norm_line_felix(fname, mname, temp, bwidth, ie, foravgshow, location, dpi, parent):

    ####################################### Initialisation #######################################
    
    data = felix_read_file(fname)
    PD=True

    if not foravgshow:
        ####################################### END Initialisation #######################################

        ####################################### Tkinter figure #######################################

        ## Embedding figure to tkinter Toplevel
        title_name = 'Normline Spectrum'
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi)
        ax = fig.add_subplot(3,1,1)
        bx = fig.add_subplot(3,1,2)
        cx = fig.add_subplot(3,1,3)
        
        ax2 = ax.twinx()
        bx2 = bx.twinx()

        #Get the baseline
        baseCal = BaselineCalibrator(fname)
        baseCal.plot(ax)
        ax.plot(data[0], data[1], ls='', marker='o', ms=3, markeredgecolor='r', c='r')
        ax.set_ylabel("cnts")
        ax.set_xlim([data[0].min()*0.95, data[0].max()*1.05])

        #Get the power and number of shots
        powCal = PowerCalibrator(fname)
        powCal.plot(bx2, ax2)

        #Get the spectrum analyser
        saCal = SpectrumAnalyserCalibrator(fname)
        saCal.plot(bx)
        bx.set_ylabel("SA")

        #Calibrate X for all the data points
        wavelength = saCal.sa_cm(data[0])

        #Normalise the intensity
        #multiply by 1000 because of mJ but ONLY FOR PD!!!
        if(PD):
            intensity = -np.log(data[1]/baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0]) *1000 
        else:
            intensity = (data[1]-baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0])

        cx.plot(wavelength, intensity, ls='-', marker='o', ms=2, c='r', markeredgecolor='k', markerfacecolor='k')
        cx.set_xlabel("wn (cm-1)")
        cx.set_ylabel("PowerCalibrated Intensity")
        
        ax.set_title(f'{fname}: {mname} at {temp}K with B0:{round(bwidth)}ms and IE:{ie}eV')

        ax.grid(True)
        bx.grid(True)
        cx.grid(True)

        export_file(fname, wavelength, intensity)

        ####################################### END Plotting details #######################################

        canvas.draw() # drawing in the tkinter canvas: canvas drawing board
        
        ####################################### END Tkinter figure #######################################

    if foravgshow:
        saCal = SpectrumAnalyserCalibrator(fname)
        wavelength = saCal.sa_cm(data[0])
        baseCal = BaselineCalibrator(fname)
        powCal = PowerCalibrator(fname)

        if(PD):
            intensity = -np.log(data[1]/baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0]) *1000 
        else:
            intensity = (data[1]-baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0])
        return wavelength, intensity
    
def felix_binning(xs, ys, delta=1):
    """
    Binns the data provided in xs and ys to bins of width delta
    output: binns, intensity 
    """
    
    #bins = np.arange(start, end, delta)
    #occurance = np.zeros(start, end, delta)
    BIN_STEP = delta
    BIN_START = xs.min()
    BIN_STOP = xs.max()

    indices = xs.argsort()
    datax = xs[indices]
    datay = ys[indices]

    print("In total we have: ", len(datax), ' data points.')
    #do the binning of the data
    bins = np.arange(BIN_START, BIN_STOP, BIN_STEP)
    print("Binning starts: ", BIN_START, ' with step: ', BIN_STEP, ' ENDS: ', BIN_STOP)

    bin_i = np.digitize(datax, bins)
    bin_a = np.zeros(len(bins)+1)
    bin_occ = np.zeros(len(bins)+1)

    for i in range(datay.size):
        bin_a[bin_i[i]] += datay[i]
        bin_occ[bin_i[i]] += 1

    binsx, data_binned = [], []
    for i in range(bin_occ.size-1):
        if bin_occ[i] > 0:
            binsx.append(bins[i]-BIN_STEP/2)
            data_binned.append(bin_a[i]/bin_occ[i])

    #non_zero_i = bin_occ > 0
    #binsx = bins[non_zero_i] - BIN_STEP/2
    #data_binned = bin_a[non_zero_i]/bin_occ[non_zero_i]

    return binsx, data_binned 

def normline_correction(*args):

    fname, location, mname, temp, bwidth, ie, foravgshow, dpi, parent = args

    try:

        folders = ["DATA", "EXPORT", "OUT"]
        back_dir = dirname(location)
        
        if set(folders).issubset(os.listdir(back_dir)): 
            os.chdir(back_dir)
            location = back_dir
            my_path = os.getcwd()
        
        else: 
            os.chdir(location)
            my_path = os.getcwd() 
            
        if(fname.find('felix')>=0):
            fname = fname.split('.')[0]

        fullname = fname + ".felix"
        basefile = fname + ".base"
        powerfile = fname + ".pow"
        files = [fullname, powerfile, basefile]

        for dirs, filenames in zip(folders, files):
            if not isdir(dirs): os.mkdir(dirs)
            if isfile(filenames): move(my_path, filenames)

        if filecheck(my_path, basefile, powerfile, fullname):
            print(f'\nFilename-->{fullname}\nLocation-->{my_path}')
            norm_line_felix(fname, mname, temp, bwidth, ie, foravgshow, location, dpi, parent)

        print("DONE")

    except Exception as e:
        ErrorInfo("ERROR:", e)

def show_baseline(fname, location, mname, temp, bwidth, ie, trap, dpi, parent):

    try:

        ####################################### Initialisation #######################################

        folders = ["DATA", "EXPORT", "OUT"]
        back_dir = dirname(location)
        
        if set(folders).issubset(os.listdir(back_dir)): 
            os.chdir(back_dir)
        
        else: 
            os.chdir(location)
            
        if(fname.find('felix')>=0):
            fname = fname.split('.')[0]

        data = felix_read_file(fname)
        baseCal = BaselineCalibrator(fname)

        ####################################### END Initialisation #######################################

        ####################################### Tkinter figure #######################################

        ## Embedding figure to tkinter Toplevel
        title_name = 'Baseline'
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi)
        ax = fig.add_subplot(111)

        ####################################### PLOTTING DETAILS #######################################

        baseCal.plot(ax)
        ax.plot(data[0], data[1], ls='', marker='o', ms=3, markeredgecolor='r', c='r')
        ax.set_xlabel("Wavenumber (cm-1)")
        ax.set_ylabel("Counts")
        ax.set_title(f'{fname}: {mname} at {temp}K and IE:{ie}eV')
        ax.grid(True)
        ax.legend(title = f'Trap:{trap}ms; B0:{round(bwidth)}ms')
        
        ####################################### END Plotting details #######################################

        canvas.draw() # drawing in the tkinter canvas: canvas drawing board
        
        ####################################### END Tkinter figure #######################################

    except Exception as e:
        ErrorInfo("Error: ", e)
