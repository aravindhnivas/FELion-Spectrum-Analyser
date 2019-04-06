#!/usr/bin/python3

## MODULES ##

## Data analysis and plotting packages
import numpy as np

# Matplotlib Modules
from matplotlib.ticker import MultipleLocator

# Tkinter Modules
from tkinter import Toplevel

## FELion modules
from FELion_normline import norm_line_felix, felix_binning
from FELion_definitions import ShowInfo, ErrorInfo, move, FELion_Toplevel

## Built-in Modules
import os
from os.path import dirname, isdir, isfile

def export_file(fname, wn, inten):
    f = open(fname.split(".pdf")[0] + '.dat','w')
    f.write("#DATA points as shown in figure: " + fname + ".pdf file!\n")
    f.write("#wn (cm-1)       intensity\n")
    for i in range(len(wn)):
        f.write("{:8.3f}\t{:8.2f}\n".format(wn[i], inten[i]))
    f.close()

def avgSpec_plot(*args):

    t, ts, lgs, minor, major, majorTickSize, markersz,\
    xlabelsz, ylabelsz, fwidth, fheight, outFilename,\
    location, mname, temp, bwidth, ie,\
    DELTA, fileNameList, dpi, parent = args

    try:

        ####################################### Initialisation #######################################

        if fileNameList == []:
            return ShowInfo("Information", "Click Select File(s)")

        folders = ["DATA", "EXPORT", "OUT"]
        back_dir = dirname(location)
        
        if set(folders).issubset(os.listdir(back_dir)): 
            os.chdir(back_dir)
            location = back_dir
            my_path = os.getcwd()
        
        else: 
            os.chdir(location)
            my_path = os.getcwd() 

        for dirs in folders:
            if not isdir(dirs): os.mkdir(dirs)

        ####################################### END Initialisation #######################################

        ####################################### Tkinter figure #######################################

        ## Embedding figure to tkinter Toplevel
        title_name = 'Average Spectrum'
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi, figsize = (fwidth, fheight))
        ax = fig.add_subplot(111)

        ####################################### PLOTTING DETAILS #######################################
        xs = np.array([], dtype='double')
        ys = np.array([], dtype='double')

        foravgshow = True
        for fname in fileNameList:
            fname = fname.split(".")[0]
            fullname = fname + ".felix"
            basefile = fname + ".base"
            powerfile = fname + ".pow"
            files = [fullname, powerfile, basefile]

            for filenames in files:
                if isfile(filenames): move(my_path, filenames)

            a,b = norm_line_felix(fname, mname, temp, bwidth, ie, foravgshow, location, dpi, parent)
            ax.plot(a, b, ls='', marker='o', ms=markersz, label=fname)
            xs = np.append(xs,a)
            ys = np.append(ys,b)

        #Binning
        binns, inten = felix_binning(xs, ys, delta=DELTA)
        ax.plot(binns, inten, ls='-', marker='', c='k')

        ax.set_xlabel(r"Calibrated lambda (cm-1)", fontsize=xlabelsz)
        ax.set_ylabel(r"Normalized Intensity", fontsize=ylabelsz)
        ax.tick_params(axis='both', which='major', labelsize=majorTickSize)

        ax.grid(True)
        ax.xaxis.set_minor_locator(MultipleLocator(minor))
        ax.xaxis.set_major_locator(MultipleLocator(major))

        l = ax.legend(title = t, fontsize = lgs)
        l.get_title().set_fontsize(ts)

        F = f'OUT/{outFilename}.pdf'
        export_file(F, binns, inten)
        fig.savefig(F)
        ####################################### END Plotting details #######################################

        canvas.draw() # drawing in the tkinter canvas: canvas drawing board
        
        ####################################### END Tkinter figure #######################################

    except Exception as e:
        ErrorInfo("ERROR", e)