## MODULES ##

# System modules
import sys
import json
import os
from os.path import dirname, isdir, isfile
from pathlib import Path as pt
import traceback

# Data analysis and plotting packages
import numpy as np

# FELion modules
from FELion_baseline_old import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
from FELion_definitions import filecheck, move

# Error traceback
import traceback

class avgPlot:

    def __init__(self, received_files, delta):

        try:
            received_files = [pt(files) for files in received_files]
            self.location = received_files[0].parent

            # Cheking if the folder contents are already created
            folders = ["DATA", "EXPORT", "OUT"]
            back_dir = self.location.parent

            if set(folders).issubset(os.listdir(back_dir)):
                os.chdir(back_dir)
                self.location = back_dir
            else:
                os.chdir(self.location)

            #print(f'Location: {self.location}')

            dataToSend = {}

            self.xs = np.array([], dtype=np.float)
            self.ys = np.array([], dtype=np.float)

            for filename in received_files:
                felixfile = filename.name
                fname = filename.stem
                basefile = f"{fname}.base"
                powerfile = f"{fname}.pow"

                self.files = [felixfile, basefile, powerfile]

                for dirs, filenames in zip(folders, self.files):
                    if not isdir(dirs):
                        os.mkdir(dirs)
                    if isfile(filenames):
                        move(self.location, filenames)
                
                if filecheck(self.location, basefile, powerfile, felixfile):
                    #print(f'\nFilename-->{felixfile}\nLocation-->{self.location}')
                    wavelength, intensity = self.norm_line_felix()
                    dataToSend[felixfile] = {"x": list(wavelength), "y": list(intensity), "name": felixfile, "mode":"markers"}

                    self.xs = np.append(self.xs, wavelength)
                    self.ys = np.append(self.ys, intensity)

            self.delta = delta
            self.binns, self.inten = self.felix_binning()
            self.avgName = "average"
            self.export_file()

            dataToSend["binns"] = {"x": list(self.binns), "y": list(self.inten), "name": f"Binn: delta={self.delta}", "mode":"lines", "line":{"color":"black"}}

            #print(f"Before JSON DATA: {dataToSend}")
            dataJson = json.dumps(dataToSend)
            print(dataJson)
                                
            #print("DONE")

        except Exception:
            err = traceback.format_exc()
            print(f"\nError occured in python code:\n{err}\n\nEND FILE")
    
    def norm_line_felix(self, PD=True):
        felixfile, basefile, powerfile = self.files

        data = felix_read_file(felixfile)

        powCal = PowerCalibrator(powerfile)
        baseCal = BaselineCalibrator(basefile)
        saCal = SpectrumAnalyserCalibrator(felixfile)

        wavelength = saCal.sa_cm(data[0])

        # Normalise the intensity
        # multiply by 1000 because of mJ but ONLY FOR PD!!!
        if(PD):
            intensity = -np.log(data[1]/baseCal.val(data[0])) / \
                powCal.power(data[0]) / powCal.shots(data[0]) * 1000
        else:
            intensity = (data[1]-baseCal.val(data[0])) / \
                powCal.power(data[0]) / powCal.shots(data[0])

        return wavelength, intensity
    
    def felix_binning(self):

        xs, ys, delta = self.xs, self.ys, self.delta
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

        #print("In total we have: ", len(datax), ' data points.')
        # do the binning of the data
        bins = np.arange(BIN_START, BIN_STOP, BIN_STEP)
        #print("Binning starts: ", BIN_START,
        #    ' with step: ', BIN_STEP, ' ENDS: ', BIN_STOP)

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

    def export_file(self):
        f = open('EXPORT/' + self.avgName + '.dat', 'w')
        f.write("#wn (cm-1)       intensity\n")
        for i in range(len(self.binns)):
            f.write("{:8.3f}\t{:8.2f}\n".format(self.binns[i], self.inten[i]))
        f.close()

if __name__ == "__main__":
    
    args = sys.argv[1:][0].split(",")
    filepaths = args[:-1]
    delta = int(args[-1])

    avgPlot(filepaths, delta)
