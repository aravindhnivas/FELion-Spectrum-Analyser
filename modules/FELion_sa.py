#!/usr/bin/python3

# Importing Modules

# DATA analysis modules
import numpy as np
from scipy.optimize import leastsq

# Tkinter Modules
from tkinter import Toplevel

# FELion Module
from FELion_definitions import ErrorInfo
from FELion_definitions import FELion_Toplevel
from FELion_baseline_old import felix_read_file

# Built-In Module
import os
from os.path import dirname

# Error traceback
import traceback

####################################### Modules Imported #######################################


class SpectrumAnalyserCalibrator(object):
    def __init__(self, felixfile, fit='linear'):
        """
        Spectrum analyser calibration initialisation
        fit can be either linear, or cubic
        """
        data = felix_read_file(felixfile)

        # Spectrum analyser calibration
        # Added 6.10.16:
        # Spectrum analyser is calibrated only above 540 cm-1, because for lower values SA gives bulshit values!
        # In case, someone does not follow the SA, value of SA < 100 will get also excluded from the fit!!!!
        sa_x = np.copy(data[0][np.logical_and(data[0] > 400, data[2] > 100)])
        sa_y = np.copy(data[2][np.logical_and(data[0] > 400, data[2] > 100)])

        if fit == 'linear':
            p0 = [1.0, 5.0]

            def fitfunc(p, x): return p[0]*x + p[1]
        elif fit == 'cubic':
            p0 = [.01, .01, 1.0, 0.0]

            def fitfunc(p, x): return p[0]*x**3 + p[1]*x**2 + p[2]*x + p[3]
        else:
            print("SA fitting function not defined!!!")

        def errfunc(p, x, y): return (fitfunc(p, x)-y)

        p, cov_p, info, mesg, ier \
            = leastsq(errfunc, p0, args=(sa_x, sa_y), full_output=1)

        if ier not in [1, 2, 3, 4] or cov_p is None:
            msg = "SA calibration optimal parameters not found: " + mesg
            raise RuntimeError(msg)
        if any(np.diag(cov_p) < 0):
            raise RuntimeError(
                "Optimal parameters not found: negative variance")

        chisq = np.dot(info["fvec"], info["fvec"])
        dof = len(info["fvec"]) - len(p)
        sigma = np.array([np.sqrt(cov_p[i, i])*np.sqrt(chisq/dof)
                          for i in range(len(p))])

        self.p = p
        self.sigma = sigma
        self.f = fitfunc
        self.data = (data[0][data[2] > 100], data[2][data[2] > 100])
        info = self.getInfo()
        print(info)

    def sa_cm(self, x):
        return self.f(self.p, x)

    def getData(self):
        return self.data

    def getInfo(self):
        info = "#Fit SA vs UNDULATOR (polynome p[0]*x**n + p[1]*x**(n-1) + ... + p[n]):\n"
        info += "#p[]     = " + "".join("{:.4e} ".format(i) for i in self.p) + \
            "\n#sigma[] = " + "".join("{:.4e} ".format(i)
                                      for i in self.sigma) + "\n"
        info += "#----------------------------------------\n"
        return info

    def plot(self, ax):
        wn, sa = self.data
        X = np.arange(wn.min(), wn.max(), 1)
        ax.plot(wn, sa, ls='', marker='s', ms=3, markeredgecolor='r', c='r')
        ax.plot(X, self.sa_cm(X), ls='-', marker='', c='g')


def FELion_Sa(felixfile, location, dpi, parent):

    ####################################### Initialisation #######################################

    folders = ["DATA", "EXPORT", "OUT"]
    back_dir = dirname(location)

    if set(folders).issubset(os.listdir(back_dir)):
        os.chdir(back_dir)
        location = back_dir

    else:
        os.chdir(location)

    ####################################### END Initialisation #######################################

    try:

        saCalibrator = SpectrumAnalyserCalibrator(felixfile, fit='cubic')

        ####################################### Tkinter figure #######################################

        # Embedding figure to tkinter Toplevel
        title_name = 'SA'
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi)
        ax = fig.add_subplot(111)

        ####################################### PLOTTING DETAILS #######################################
        saCalibrator.plot(ax)

        ax.set_title(f'Spectrum analyser calibration from {felixfile} file')
        ax.set_xlabel("wn set (cm-1)")
        ax.set_ylabel("wn SA (cm-1)")

        ####################################### END Plotting details #######################################

        canvas.draw()  # drawing in the tkinter canvas: canvas drawing board

        ####################################### END Tkinter figure #######################################
    except:
        ErrorInfo('Error: ', traceback.format_exc())
