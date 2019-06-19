# Importing Modules

# System modules
import sys
import json
import os
from os.path import dirname, isdir, isfile
from pathlib import Path as pt
import traceback

# Data analysis
import numpy as np

# FELion-Modules
from FELion_baseline_old import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
from FELion_definitions import filecheck, move

######################################################################################


class normplot:
    def __init__(self, received_files):

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

            dataToSend = {}

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
                    dataToSend[felixfile] = {"x": list(wavelength), "y": list(intensity), "name": felixfile, "mode":"lines"}
                    self.export_file(fname, wavelength, intensity)

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

    def export_file(self, fname, wn, inten):
        f = open('EXPORT/' + fname + '.dat', 'w')
        f.write("#DATA points as shown in lower figure of: " + fname + ".pdf file!\n")
        f.write("#wn (cm-1)       intensity\n")
        for i in range(len(wn)):
            f.write("{:8.3f}\t{:8.2f}\n".format(wn[i], inten[i]))
        f.close()


if __name__ == "__main__":

    args = sys.argv[1:][0].split(",")
    filepaths = args
    normplot(filepaths)