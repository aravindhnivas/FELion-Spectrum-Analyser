# Importing Modules

# System modules
import sys
import json
import os
import shutil
from os.path import isdir, isfile
from pathlib import Path as pt
import traceback

# Data analysis
import numpy as np

# FELion modules
from FELion_baseline_old import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
from baseline import Create_Baseline

# Tkinter modules
from tkinter import Tk, messagebox

######################################################################################

colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
          (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
          (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
          (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
          (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]


class normplot:

    def __init__(self, received_files, delta):

        try:
            self.delta = delta
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
            
            dataToSend = {"felix": {}, "base": {}}
            #dataToSend["params"] = {"location":f"{self.location}"}

            c = 0

            for filename in received_files:

                felixfile = filename.name
                fname = filename.stem
                basefile = f"{fname}.base"
                powerfile = f"{fname}.pow"

                self.fietypes = [felixfile, basefile, powerfile]

                for folder, filetype in zip(folders, self.fietypes):
                    if not isdir(folder):
                        os.mkdir(folder)
                    if isfile(filetype):
                        shutil.move(self.location.joinpath(filetype),
                                    self.location.joinpath("DATA", filetype))

                #if self.filecheck(basefile, powerfile):
                wavelength, intensity = self.norm_line_felix()
                wavelength, intensity = self.felix_binning(wavelength, intensity)

                dataToSend["felix"][f"{felixfile}_histo"] = {"x": list(wavelength), "y": list(intensity), "name": f"{filename.stem}_bar","type": "bar","xaxis": "x2", "yaxis": "y2","marker": {"color": f"rgb{colors[c]}"}}
                dataToSend["felix"][felixfile] = {"x": list(wavelength), "y": list(intensity),"name": f"{filename.stem}_norm", "type": "scatter", "xaxis": "x2", "yaxis": "y2","line": {"color": f"rgb{colors[c]}"}}

                self.export_file(fname, wavelength, intensity)

                basefile_data = np.array(Create_Baseline(felixfile, self.location, plotIt=False).get_data())
                #print(f"Basefile_data: {basefile_data}\n{basefile_data.shape}\n[0]{basefile_data[0]}\n{basefile_data[0].shape}\n\n[1, 0]{basefile_data[1][0]}\n{basefile_data[1][0].shape}")

                # Ascending order sort by wn
                base_line = basefile_data[1][0]
                base_line = np.take(base_line, base_line[0].argsort(), 1).tolist()
                base_felix = basefile_data[0]
                base_felix = np.take(base_felix, base_felix[0].argsort(), 1).tolist()
                #print(f"Base_line: {base_line}\nBase_felix: {base_felix}")

                dataToSend["base"][f"{felixfile}_base"] = {"x": list(base_felix[0]), "y": list(base_felix[1]), "name": f"{filename.stem}_felix", "mode": "lines", "line": {"color": f"rgb{colors[c]}"}}
                dataToSend["base"][f"{felixfile}_line"] = {"x": list(base_line[0]), "y": list(base_line[1]), "name": f"{filename.stem}_base", "mode": "lines+markers", "marker": {"color": "black"}}

                # Logging file status of powerfiles and basefiles
                #dataToSend["params"]["powerfiles"] = {powerfile:self.location.joinpath("DATA", powerfile).exists()}
                #dataToSend["params"]["basefiles"] = {basefile:self.location.joinpath("DATA", basefile).exists()}

                #dataToSend["params"]["powerfiles"] = {f"{powerfile}":self.powerfile_status}
                #dataToSend["params"]["basefiles"] = {f"{basefile}":self.basefile_status}
                c += 1

            #print(f"Before JSON DATA: {dataToSend}")
            dataJson = json.dumps(dataToSend)
            print(dataJson)

            # print("DONE")

        except Exception:
            err = traceback.format_exc()
            print(f"\nError occured in python code:\n{err}\n\nEND FILE")

    def norm_line_felix(self, PD=True):

        felixfile, basefile, powerfile = self.fietypes

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

    def export_file(self, fname, wn, inten):

        f = open('EXPORT/' + fname + '.dat', 'w')
        f.write("#DATA points as shown in lower figure of: " +
                fname + ".pdf file!\n")
        f.write("#wn (cm-1)       intensity\n")
        for i in range(len(wn)):
            f.write("{:8.3f}\t{:8.2f}\n".format(wn[i], inten[i]))
        f.close()

    def felix_binning(self, xs, ys):

        delta = self.delta
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

    def filecheck(self, basefile, powerfile):

        # Powefile check
        if not self.location.joinpath("DATA", powerfile).exists():
            if self.location.joinpath("Pow", powerfile).exists():
                shutil.move(self.location.joinpath("Pow", powerfile), self.location.joinpath("DATA", powerfile))

            elif self.location.joinpath(powerfile).exists():
                shutil.move(self.location.joinpath(powerfile), self.location.joinpath("DATA", powerfile))

            else:
                self.powerfile_status = False
                return False

        # Basefile check
        if not self.location.joinpath("DATA", basefile).exists():
            if self.location.joinpath(basefile).exists():
                shutil.move(self.location.joinpath(basefile), self.location.joinpath("DATA", basefile))
            else:
                self.basefile_status = False
                return False

        self.powerfile_status = True
        self.basefile_status = True

        return True

if __name__ == "__main__":

    args = sys.argv[1:][0].split(",")
    filepaths = args[:-1]
    delta = float(args[-1])
    normplot(filepaths, delta)