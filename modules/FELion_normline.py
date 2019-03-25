#!/usr/bin/python3

# FELion-Modules
from FELion_baseline import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
from FELion_definitions import ShowInfo, ErrorInfo, filecheck, move

# DATA Analysis modules:
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, messagebox

# Built-In modules
import os, shutil
from os.path import dirname, isdir, isfile, join


################################################################################

def export_file(fname, wn, inten):
    f = open('EXPORT/' + fname + '.dat','w')
    f.write("#DATA points as shown in lower figure of: " + fname + ".pdf file!\n")
    f.write("#wn (cm-1)       intensity\n")
    for i in range(len(wn)):
        f.write("{:8.3f}\t{:8.2f}\n".format(wn[i], inten[i]))
    f.close()

def norm_line_felix(fname, mname, temp, bwidth, ie, save, foravgshow, show, dpi):

    """
    Reads data from felix meassurement file and 
    calculates the calibrated wavenumber and calibrated/normalised
    intensity for every single poitnt
    1. for this to work, baseline, power and num_shots data has to be present! 

    Input: filename       save = False by default (produce output pdf file)
    Output: data[0,1]     0 - wavenumber, 1 - intensity
    """

    if(fname.find('DATA')):
        fname = fname.split('/')[-1]

    if(fname.find('felix')):
        fname = fname.split('.')[0]
    
    data = felix_read_file(fname)
    PD=True

    if not foravgshow:
        fig = plt.figure(figsize=(8, 8), dpi = dpi)
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
        
        ax.set_title(f'{fname}: {mname} at {temp}K with B0:{round(bwidth)}ms and IE:{ie}eV')

        if save:
            fname = fname.replace('.','_')
            plt.savefig('OUT/'+fname+'.pdf')
            export_file(fname, wavelength, intensity)

        if show:
            plt.show()

        plt.close()

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

def main(s=True, plotShow=False):
    my_path = os.getcwd()
    raw_filename = str(input("Enter the file name (without .felix): "))
    filename = raw_filename + ".felix"
    powerfile = raw_filename + ".pow"
    fname = filename

    if isfile(powerfile):
        shutil.copyfile(my_path + "/{}".format(powerfile), my_path + "/DATA/{}".format(powerfile))
        print("Powerfile copied to the DATA folder.")
    else:
        print("\nCAUTION:You don't have the powerfile(.pow)\n")

    a,b = norm_line_felix(fname)
    print(a, b)
    print("\nProcess Completed.\n")


def normline_correction(*args):
    fname, location, mname, temp, bwidth, ie, save, foravgshow, normall, fileNameList, show, dpi = args
    print(f'\nPlotAll-->{normall}\nShow-->{show}\nSave-->{save}')

    try:
        folders = ["DATA", "EXPORT", "OUT"]
        back_dir = dirname(location)
        
        if set(folders).issubset(os.listdir(back_dir)): 
            os.chdir(back_dir)
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

        if not normall:
            if filecheck(my_path, basefile, powerfile, fullname):
                norm_line_felix(fname, mname, temp, bwidth, ie, save, foravgshow, show, dpi)
            if save and isfile(join(my_path, 'OUT', f'{fname}.pdf')): ShowInfo('SAVED', f'File {fname}.pdf for {fullname} saved in /OUT directory.')

        if normall:
            print(f'\nFile Lists-->{fileNameList}\nTotal files-->{len(fileNameList)}')

            if len(fileNameList) is 0: return ShowInfo('Select File(s)', 'Please select Files')

            for fname in fileNameList:
                fname = fname.split(".")[0]
                fullname = fname + ".felix"
                powerfile = fname + ".pow"
                basefile = fname + ".base"

                if filecheck(my_path, basefile, powerfile, fullname):
                    print(f'\nRunning File-->{fullname}')
                    norm_line_felix(fname, mname, temp, bwidth, ie, save, foravgshow, show, dpi)

                print('\nNext File')

            if save: ShowInfo('SAVED', f'Files are saved in /OUT directory.')

        print("DONE")

    except Exception as e:
        ErrorInfo("ERROR:", e)

def show_baseline(fname, location, mname, temp, bwidth, ie, trap, dpi):

    try:
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

        base1 = plt.figure(dpi = dpi)
        base = base1.add_subplot(1,1,1)
        baseCal.plot(base)
        base.plot(data[0], data[1], ls='', marker='o', ms=3, markeredgecolor='r', c='r')
        base.set_xlabel("Wavenumber (cm-1)")
        base.set_ylabel("Counts")
        base.set_title(f'{fname}: {mname} at {temp}K and IE:{ie}eV')
        base.grid(True)
        base.legend(title = f'Trap:{trap}ms; B0:{round(bwidth)}ms')
        plt.savefig('OUT/'+fname+'_baseline.png')
        plt.show()
        plt.close()

    except Exception as e:
        ErrorInfo("Error: ", e)
