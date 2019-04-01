#!/usr/bin/python3

## Importing Modules

# FELion-Modules
from FELion_baseline import felix_read_file, BaselineCalibrator
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator
from FELion_definitions import ShowInfo, ErrorInfo, filecheck, move

# DATA Analysis modules:
import matplotlib.pyplot as plt
import numpy as np

# Embedding Matplotlib in tkinter window
from tkinter import *
from tkinter import ttk

# Matplotlib Modules for tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

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

def norm_line_felix(fname, mname, temp, bwidth, ie, foravgshow, dpi, parent):
    
    data = felix_read_file(fname)
    PD=True

    if not foravgshow:
        root = Toplevel(master = parent)
        root.wm_title("Power Calibrated/Normalised Spectrum")

        ################################ PLOTTING DETAILS ########################################

        fig = Figure(figsize=(8, 8), dpi = dpi)
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

        ##################################################################################################
        ##################################################################################################

        # Drawing in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master = root)
        canvas.draw()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = 1)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = 1)

        frame = Frame(root, bg = 'light grey')
        frame.pack(side = 'bottom', fill = 'both', expand = True)

        label = Label(frame, text = 'Save as:')
        label.pack(side = 'left', padx = 15, ipadx = 10, ipady = 5)

        name = StringVar()
        filename = Entry(frame, textvariable = name)
        name.set(fname)
        filename.pack(side = 'left')

        def save_func():
            fig.savefig(f'OUT/{name.get()}.pdf')
            export_file(fname, wavelength, intensity)
            if isfile(f'OUT/{name.get()}.pdf'): ShowInfo('SAVED', f'File: {name.get()}.pdf saved in OUT/ directory')

        button = ttk.Button(frame, text = 'Save', command = lambda: save_func())
        button.pack(side = 'left', padx = 15, ipadx = 10, ipady = 5)

        def on_key_press(event): 
            key_press_handler(event, canvas, toolbar)

            if event.key == 'c':
                fig.savefig(f'OUT/{name.get()}.pdf')
                export_file(fname, wavelength, intensity)
                if isfile(f'OUT/{name.get()}.pdf'): ShowInfo('SAVED', f'File: {name.get()}.pdf saved in OUT/ directory')

        canvas.mpl_connect("key_press_event", on_key_press)
        root.mainloop()

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
    fname, location, mname, temp, bwidth, ie, foravgshow, dpi, parent = args

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

        if filecheck(my_path, basefile, powerfile, fullname):
            print(f'\nFilename-->{fullname}\nLocation-->{my_path}')
            norm_line_felix(fname, mname, temp, bwidth, ie, foravgshow, dpi, parent)

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
