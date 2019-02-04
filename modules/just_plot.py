
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.interpolate import interp1d as interpolate

def theory_exp(filelists,exp,location, save, show):

        os.chdir(location)

        plt.figure(dpi=100)
        e = np.genfromtxt(exp)
        xe, ye = e[:,0], e[:,1]

        plt.plot(xe,ye, label='Exp')
        for i, c, l in zip(filelists, ('k','r'), (5,5)):
                t = np.genfromtxt(i, comments='F')
                xt, yt = t[:,0], t[:,1]
                yt = (yt/yt.max())*ye.max()
                plt.vlines(xt, ymin=0, ymax=yt,\
                        lw = l, color = c,\
                        label = i.split('/')[-1].split('.')[0])
        
        plt.legend()
        plt.title('Theory vs Exp: %s'%exp.split('/')[-1].split('.')[0])
        plt.xlabel('Wavenumber $cm^{-1}$')
        plt.ylabel('Normalised Intensity \n(Theory Inten. is norm. to Exp.)')
        plt.xlim(xmax = xe.max()+50, xmin = xe.min()-50)
        plt.ylim(ymin=0)
        plt.tight_layout()
        if save: plt.savefig('theory-exp_%s.png'%exp.split('/')[-1].split('.')[0])
        if show: plt.show()
        plt.close()

def power_plot(powerfiles, location, save,show):

        os.chdir(location)
        plt.figure()
        for powerfile in powerfiles:
                f = open(powerfile)
                for i in f:
                        if i.find('#SHOTS')>=0:
                                shots=i.strip().split('=')[-1]
                                break
                f.close()

                shots = np.float(shots)

                power_file = np.genfromtxt(powerfile)
                power_file_extrapolate = interpolate(power_file[:,0], power_file[:,1], kind = 'linear', fill_value = 'extrapolate')

                temp = np.genfromtxt(powerfile.split('.')[0]+'.felix')
                x = temp[:,0]

                power_extrapolated = power_file_extrapolate(x)

                plt.title("Power calibration\n Filename: %s"%powerfile)

                plt.plot(power_file[:,0], power_file[:,1], 'ok',ms=7)
                plt.plot(x, power_extrapolated, '-', label=powerfile+':'+str(shots))
        
        plt.legend()
        plt.title('Power from .pow file')
        plt.ylabel('Power (mJ)')

        if show: plt.show()
        if save: plt.savefig('power_combined.png')
        plt.close()