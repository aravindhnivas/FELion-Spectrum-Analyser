#!/usr/bin/python3

import numpy as np
import pylab as P
import sys
import copy
from scipy.optimize import leastsq
from scipy.interpolate import interp1d
from FELion_baseline import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
import os

# Custom inport:
import matplotlib.pyplot as plt
from tkinter import Tk, messagebox

from FELion_definitions import *
from os.path import dirname, isdir, isfile, join
import shutil
import glob

################################################################################
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

class Normline_class:
    def __init__(self, *args):

        self.fname, self.location, self.mname, self.temp, self.bwidth, self.ie, self.save, self.foravgshow, self.normall, self.fileNameList, self.show = args

        
        self.back_dir = dirname(self.location)
        self.folders = ["DATA", "EXPORT", "OUT"]

        if set(self.folders).issubset(os.listdir(self.back_dir)): self.location = self.back_dir

        self.for_normall_saveDialog = False
        if self.normall: self.for_normall_saveDialog = True
        
        self.fname = self.fname.split('.')[0]
        self.fullname = self.fname + ".felix"
        self.basefile = self.fname + ".base"
        self.powerfile = self.fname + ".pow"
        self.files = [self.fullname, self.powerfile, self.basefile]

        for dirs, filenames in zip(self.folders, self.files):
            if not isdir(dirs): os.mkdir(dirs)
            if isfile(filenames): move(self.location, filenames)
        
        os.chdir(self.location)

    def plot(self):
        try:
            if self.normall:
                for fname in self.fileNameList:
                    fname = fname.split(".")[0]

                    self.fname = fname
                    self.fullname = fname + ".felix"
                    self.powerfile = fname + ".pow"
                    self.basefile = fname + ".base"

                    self.normrun()
                self.completed()

            else:
                print(
                    "\nFilename --> {}\nLocation --> {}\nMolecule --> {}\nTemp --> {}\nB0 --> {}\nIE --> {}".format(
                        self.fullname, self.location, self.mname, self.temp, self.bwidth, self.ie
                        )
                )
                self.normrun()

        except Exception as e:
            ErrorInfo("ERROR:", e)
  
    def normrun(self):
        # checking:
        file = join(self.location, "DATA", self.fullname)
        file1 = join(self.location, self.fullname)
        move_file = (self.location, self.fullname)

        pfile = join(self.location, "DATA", self.powerfile)
        pfile1 = join(self.location, "Pow", self.powerfile)
        move_pfile1 = (self.location, "Pow", self.powerfile)
        pfile2 = join(self.location, self.powerfile)
        move_pfile2 = (self.location, self.powerfile)

        bfile = join(self.location, "DATA", self.basefile)
        bfile1 = join(self.location, self.basefile)
        move_bfile = (self.location, self.basefile)

        #File check
        if not isfile(file):
            if isfile(file1):
                move(*move_file)
            else:
                return ErrorInfo("ERROR: ", "File %s NOT found"%self.fullname)

        #Basefile check
        if not isfile(bfile):
            if isfile(bfile1):
                move(*move_bfile)
            else:
                return ErrorInfo("ERROR: ", "Basefile: %s NOT found"%self.basefile)

        #Powefile check
        if not isfile(pfile):
            if isfile(pfile1):
                move1(*move_pfile1)
        
            elif isfile(pfile2):
                move(*move_pfile2)
            
            else:
                return ErrorInfo("ERROR: ", "Powerfile: %s NOT found"%self.powerfile)
        
        #Normline run
        self.norm_line_felix()

        #printing confirmation
        file_check = join(self.location, 'OUT', self.fname+'.pdf')
        if not self.for_normall_saveDialog:
            if isfile(file_check) and self.save:
                ShowInfo("SAVED", "File %s.pdf saved in OUT/ directory"%self.fname)

    def completed(self):
        for fname in self.fileNameList:
            fname = fname.split(".")[0]

            file_check = join(self.location, 'OUT', fname+'.pdf')
            
            if isfile(file_check) and self.save:
                ShowInfo("SAVED", "File %s.pdf saved in OUT/ directory"%fname)

    def norm_line_felix(self):
        
        data = felix_read_file(self.fname)
        PD=True

        if not self.foravgshow:
            #plt.rcParams['figure.figsize'] = [8,10]
            plt.rcParams['figure.dpi'] = 80
            plt.rcParams['savefig.dpi'] = 100
            fig = plt.figure(figsize=(8,10), )
            ax = fig.add_subplot(3,1,1)
            bx = fig.add_subplot(3,1,2)
            cx = fig.add_subplot(3,1,3)
            ax2 = ax.twinx()
            bx2 = bx.twinx()

            #Get the baseline
            baseCal = BaselineCalibrator(self.fname)
            baseCal.plot(ax)
            ax.plot(data[0], data[1], ls='', marker='o', ms=3, markeredgecolor='r', c='r')
            ax.set_ylabel("cnts")
            ax.set_xlim([data[0].min()*0.95, data[0].max()*1.05])

            #Get the power and number of shots
            powCal = PowerCalibrator(self.fname)
            powCal.plot(bx2, ax2)


            #Get the spectrum analyser
            saCal = SpectrumAnalyserCalibrator(self.fname)
            saCal.plot(bx)
            bx.set_ylabel("SA")
            

            #Calibrate X for all the data points
            self.wavelength = saCal.sa_cm(data[0])

            #Normalise the intensity
            #multiply by 1000 because of mJ but ONLY FOR PD!!!
            if(PD):
                self.intensity = -np.log(data[1]/baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0]) *1000 
            else:
                self.intensity = (data[1]-baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0])

            cx.plot(self.wavelength, self.intensity, ls='-', marker='o', ms=2, c='r', markeredgecolor='k', markerfacecolor='k')
            cx.set_xlabel("wn (cm-1)")
            
            ax.set_title("Filename: {}, for {}, at temp: {}K,\nB0: {}ms and IE(eV): {}".format(self.fname, self.mname, self.temp, self.bwidth, self.ie))

            if self.save:
                self.fname = self.fname.replace('.','_')
                plt.savefig('OUT/'+self.fname+'.pdf')
                self.export_file()

            if self.show:
                plt.show()
            
            plt.close()

            # save baseline
            if self.save:
                base1 = plt.figure(dpi = 100)
                base = base1.add_subplot(1,1,1)
                baseCal.plot(base)
                base.plot(data[0], data[1], ls='', marker='o', ms=3, markeredgecolor='r', c='r')
                plt.xlabel("Wavenumber (cm-1)")
                plt.ylabel("Counts")
                plt.title("Baseline: Filename: {}, for {} ".format(self.fname, self.mname))
                plt.savefig('OUT/'+self.fname+'_baseline.png')
                plt.close()

        if self.foravgshow:
            saCal = SpectrumAnalyserCalibrator(self.fname)
            self.wavelength = saCal.sa_cm(data[0])
            baseCal = BaselineCalibrator(self.fname)
            powCal = PowerCalibrator(self.fname)

            if(PD):
                self.intensity = -np.log(data[1]/baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0]) *1000 
            else:
                self.intensity = (data[1]-baseCal.val(data[0])) / powCal.power(data[0]) / powCal.shots(data[0])
            return self.wavelength, self.intensity
    
    def export_file(self):
        f = open('EXPORT/' + self.fname + '.dat','w')
        f.write("#DATA points as shown in lower figure of: " + self.fname + ".pdf file!\n")
        f.write("#wn (cm-1)       intensity\n")
        for i in range(len(self.wavelength)):
            f.write("{:8.3f}\t{:8.2f}\n".format(self.wavelength[i], self.intensity[i]))
        f.close()
    
    def show_baseline(self):
    
        try:
            data = felix_read_file(self.fname)
            baseCal = BaselineCalibrator(self.fname)

            base1 = plt.figure(dpi = 100)
            base = base1.add_subplot(1,1,1)
            baseCal.plot(base)
            base.plot(data[0], data[1], ls='', marker='o', ms=3, markeredgecolor='r', c='r')
            plt.xlabel("Wavenumber (cm-1)")
            plt.ylabel("Counts")
            plt.title("Baseline: Filename: {}, for {} ".format(self.fname, self.mname))
            plt.show()
            if self.save: 
                plt.savefig('OUT/'+self.fname+'_baseline.png')
                ShowInfo('Saved:', 'File %s saved'%self.fname+'_baseline.png')
            plt.close()

        except Exception as e:
            ErrorInfo("Error: ", e)