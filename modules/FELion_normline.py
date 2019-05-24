#!/usr/bin/python3

# Importing Modules

# DATA Analysis modules:
import numpy as np

# Built-In modules
import os
from os.path import dirname, isdir, isfile

# FELion-Modules
from FELion_baseline_old import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
from FELion_definitions import ShowInfo, ErrorInfo, filecheck, move, FELion_Toplevel

# Tkinter Modules
from tkinter import Toplevel

# Error traceback
import traceback

# Matplotlib
import matplotlib.pyplot as plt

################################################################################


def export_file(fname, wn, inten):
    f = open('EXPORT/' + fname + '.dat', 'w')
    f.write("#DATA points as shown in lower figure of: " + fname + ".pdf file!\n")
    f.write("#wn (cm-1)       intensity\n")
    for i in range(len(wn)):
        f.write("{:8.3f}\t{:8.2f}\n".format(wn[i], inten[i]))
    f.close()


def norm_line_felix(felixfile, mname, temp, bwidth, ie, foravgshow, location, dpi, parent, hd=False, trap=None):

    ####################################### Initialisation #######################################

    data = felix_read_file(felixfile)

    fname = felixfile.split('.')[0]
    basefile = f'{fname}.base'
    powerfile = f'{fname}.pow'

    PD = True

    def plot(ax, bx, cx):

        #ax2 = ax.twinx() # Shots
        bx2 = bx.twinx() # Power
        
        if hd:
            ms0, ms1, ms2, ms3, ms4  = 1, 1, 2, 2, 1 # Baseline, felix, power, SA, Normalised
        elif not hd:
            ms0, ms1, ms2, ms3, ms4 = 5, 3, 3, 5, 2 
        else:
            ms0, ms1, ms2, ms3, ms4 = None, None, None, None, None
        
        print('Markers:', ms0, ms1, ms2, ms3, ms4)

        # Get the power and number of shots
        powCal = PowerCalibrator(powerfile, ms=ms2)
        powCal.plot(bx2) # Power, Shots

        # Get the baseline
        baseCal = BaselineCalibrator(basefile, ms0)
        baseCal.plot(ax)
        ax.plot(data[0], data[1], '.--',
                ms=ms1, markeredgecolor='r', c='r', label='Felix: %i Shots'%powCal.shots(data[0])[0])
        
        # Get the spectrum analyser
        saCal = SpectrumAnalyserCalibrator(felixfile, ms=ms3)
        saCal.plot(bx)

        # Calibrate X for all the data points
        wavelength = saCal.sa_cm(data[0])

        # Normalise the intensity
        # multiply by 1000 because of mJ but ONLY FOR PD!!!
        if(PD):
            intensity = -np.log(data[1]/baseCal.val(data[0])) / \
                powCal.power(data[0]) / powCal.shots(data[0]) * 1000
        else:
            intensity = (data[1]-baseCal.val(data[0])) / \
                powCal.power(data[0]) / powCal.shots(data[0])

        cx.plot(wavelength, intensity, ls='-', marker='o', ms=ms4,
                c='r', markeredgecolor='k', markerfacecolor='k', label='Normalised')

                
        if not hd: 

            # Labels
            ax.set_ylabel("Counts")
            bx.set_ylabel("SA $(cm^{-1})$")

            bx2.legend(fontsize=10, loc='lower right')
            #ax2.legend(fontsize=10, loc='lower right')
            return wavelength, intensity

        else:

            # Labels
            ax.set_ylabel("Counts", fontsize=7)
            bx.set_ylabel("SA $(cm^{-1})$", fontsize=7)

            bx2.legend(fontsize=6, loc='lower right')
            #ax2.legend(fontsize=6)
        
    if not foravgshow:

        if not hd:

            title_name = 'Normline Spectrum'
            root = Toplevel(parent)
            tk_widget = FELion_Toplevel(root, title_name, location)

            fig, canvas = tk_widget.figure(dpi)
            ax = fig.add_subplot(311, )
            bx = fig.add_subplot(312, sharex=ax)
            cx = fig.add_subplot(313, sharex=ax)

            wavelength, intensity = plot(ax, bx, cx)
            mname = '$%s$'%mname
            ax.set_title(f'{felixfile}: {mname} at {temp}K; B0:{round(bwidth)}ms; Trap:{trap}ms and IE:{ie}eV')
            cx.set_xlabel("Calibrated wavelength $(cm^{-1})$")
            cx.set_ylabel("Normalised Intensity")

            for i in (ax, bx, cx):
                i.grid()
            ax.legend()
            bx.legend(loc='upper left')
            cx.legend()
                
            canvas.draw()

            export_file(fname, wavelength, intensity)

        if hd:
            with plt.style.context(['science']):

                # Making Figure
                fig_, (ax_, bx_, cx_) = plt.subplots(3,1, sharex=True, gridspec_kw={'hspace':0})
                
                # PLotting
                plot(ax_, bx_, cx_)

                # Legends
                ax_lg = f'B_0={round(bwidth)}ms; Trap={trap}ms'
                l0 = ax_.legend(title='$%s$'%ax_lg, fontsize=5)
                l0.get_title().set_fontsize(5)

                bx_.legend(fontsize=6, loc='upper left')

                cx_lg = f'{temp}K;{ie}eV'
                l1 = cx_.legend(title='$%s$'%cx_lg, fontsize=5)
                l1.get_title().set_fontsize(5)

                # Title and labels
                fname1 = felixfile.replace('_', '/')
                title = f'{fname1}: {mname}'
                ax_.set_title('$%s$'%title, fontsize=10)

                cx_.set_xlabel("Calibrated wavelength $(cm^{-1})$", fontsize=7)
                cx_.set_ylabel("Intensity", fontsize=7)

                # Making labels invisible
                for i in (ax_, bx_, cx_):
                    i.label_outer()
                    #i.grid()

                # Saving Figure
                fig_.savefig(f'./OUT/{fname}_high_res.pdf', dpi=dpi*3)
                fig_.savefig(f'./OUT/{fname}_high_res.png', dpi=dpi*3)

                
    if foravgshow:
        saCal = SpectrumAnalyserCalibrator(felixfile)
        wavelength = saCal.sa_cm(data[0])
        baseCal = BaselineCalibrator(basefile)
        powCal = PowerCalibrator(powerfile)

        if(PD):
            intensity = -np.log(data[1]/baseCal.val(data[0])) / \
                powCal.power(data[0]) / powCal.shots(data[0]) * 1000
        else:
            intensity = (data[1]-baseCal.val(data[0])) / \
                powCal.power(data[0]) / powCal.shots(data[0])
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
    # do the binning of the data
    bins = np.arange(BIN_START, BIN_STOP, BIN_STEP)
    print("Binning starts: ", BIN_START,
          ' with step: ', BIN_STEP, ' ENDS: ', BIN_STOP)

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


def normline_correction(*args, **kw):

    fname, location, mname, temp, bwidth, ie, foravgshow, dpi, parent = args

    try:
        fullname = fname
        folders = ["DATA", "EXPORT", "OUT"]
        back_dir = dirname(location)

        if set(folders).issubset(os.listdir(back_dir)):
            os.chdir(back_dir)
            location = back_dir
            my_path = os.getcwd()

        else:
            os.chdir(location)
            my_path = os.getcwd()

        if(fname.find('felix') >= 0):
            fname = fname.split('.')[0]

        basefile = fname + ".base"
        powerfile = fname + ".pow"
        files = [fullname, powerfile, basefile]

        for dirs, filenames in zip(folders, files):
            if not isdir(dirs):
                os.mkdir(dirs)
            if isfile(filenames):
                move(my_path, filenames)

        if filecheck(my_path, basefile, powerfile, fullname):
            print(f'\nFilename-->{fullname}\nLocation-->{my_path}')

            if not kw['hd']:
                norm_line_felix(fullname, mname, temp, bwidth, ie,
                                foravgshow, location, dpi, parent, trap=kw['trap'])
            else:
                norm_line_felix(fullname, mname, temp, bwidth, ie,
                                foravgshow, location, dpi, parent, hd=True, trap=kw['trap'])
                ShowInfo('Done', 
                    f'Completed\nFile {fname}_high_red.pdf and {fname}_high_red.png saved in /OUT directory\nLocation: {location}')

        print("DONE")

    except:
        ErrorInfo('Error: ', traceback.format_exc())