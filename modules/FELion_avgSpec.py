#!/usr/bin/python3
import os
import numpy as np
import pylab as P
import sys
import copy 
from os import path
from scipy.optimize import leastsq
from FELion_normline import norm_line_felix
from FELion_normline import felix_binning
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, NullFormatter, NullLocator
import matplotlib.pyplot as plt

## modules
import os
from tkinter import Tk, messagebox

DELTA=2.0

def export_file(fname, wn, inten):
    f = open(fname + '.dat','w')
    f.write("#DATA points as shown in figure: " + fname + ".pdf file!\n")
    f.write("#wn (cm-1)       intensity\n")
    for i in range(len(wn)):
        f.write("{:8.3f}\t{:8.2f}\n".format(wn[i], inten[i]))
    f.close()

def main(**kwargs):
    t="Title"
    ts=10
    lgs=5
    minor=5
    major=50
    majorTickSize=8
    xmin=1000
    xmax=2000

    fig = plt.subplot(1,1,1)
    plt.rcParams['figure.figsize'] = [6,4]
    plt.rcParams['figure.dpi'] = 80
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['font.size'] = ts # Title Size
    plt.rcParams['legend.fontsize'] = lgs # Legend Size

    my_path = os.getcwd() # getting current directory
    pwd = os.listdir(my_path + r"\DATA") # going into the data folder to fetch all the available data filename.
    fileNameList = [] # creating a varaiable list : Don't add any data here. You can use the script as it is since it automatically takes the data in the DATA folder
    for p in pwd:
        if p.endswith(".felix"): # finding the files only with .felix extension
            filename = os.path.basename(p) # getting the name of the file
            file = os.path.splitext(filename)[0] # printing only the file name without the extension .felix
            fileNameList.append([file]) # saving all the file names in the variable list fileNameList
        else:
            continue
            
    xs = np.array([],dtype='double')
    ys = np.array([],dtype='double')

    for l in fileNameList:
        a,b = norm_line_felix(l[0])
        fig.plot(a, b, ls='', marker='o', ms=1, label=l[0])
        xs = np.append(xs,a)
        ys = np.append(ys,b)
    fig.legend(title=t) #Set the fontsize for each label

    #Binning
    binns, inten = felix_binning(xs, ys, delta=DELTA)
    fig.plot(binns, inten, ls='-', marker='', c='k')

    #Exporting the Binned file.
    F = 'OUT/average_Spectrum.pdf'
    export_file(F, binns, inten)

    #Set the Xlim values and fontsizes.
    fig.set_xlim([xmin,xmax])
    fig.set_xlabel(r"Calibrated lambda (cm-1)", fontsize=10)
    fig.set_ylabel(r"Normalized Intensity", fontsize=10)
    fig.tick_params(axis='both', which='major', labelsize=majorTickSize)

    #Set the Grid value False if you don't need it.
    fig.grid(True)
    #Set the no. of Minor and Major ticks.
    fig.xaxis.set_minor_locator(MultipleLocator(minor))
    fig.xaxis.set_major_locator(MultipleLocator(major))
    plt.savefig(F)
    plt.close()
    print("Completed.")
    print()

def avgSpec_plot(t, ts, lgs, minor, major, \
                majorTickSize, xmin, xmax, outFilename,\
                location, mname, temp, bwidth, ie,\
                specificFiles, allFiles
                ):

    # Custom definitions:

    def filesaved():
        if os.path.isfile(my_path+r"\OUT\{}.pdf".format(outFilename)):
            root = Tk()
            root.withdraw()
            messagebox.showinfo("Information", "File '{}.pdf' Saved".format(outFilename))
            root.destroy()

    def filenotfound():
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", "FILE NOT FOUND")
        root.destroy()
    
    show = False
    os.chdir(location)
    my_path = os.getcwd()

    try:
        fig = plt.subplot(1,1,1)
        plt.rcParams['figure.figsize'] = [6,4]
        plt.rcParams['figure.dpi'] = 80
        plt.rcParams['savefig.dpi'] = 100
        plt.rcParams['font.size'] = ts # Title Size
        plt.rcParams['legend.fontsize'] = lgs # Legend Size

        pwd = os.listdir(my_path + r"\DATA") # going into the data folder to fetch all the available data filename.
        fileNameList = [] # creating a varaiable list : Don't add any data here. You can use the script as it is since it automatically takes the data in the DATA folder
        for f in pwd:
            if f.find(".felix")>=0:
                fileNameList.append(f.split(".felix")[0])

        xs = np.array([],dtype='double')
        ys = np.array([],dtype='double')

        if all and not specificFiles:
            for filelist in fileNameList:
                a,b = norm_line_felix(filelist, mname, temp, bwidth, ie)
                fig.plot(a, b, ls='', marker='o', ms=1, label=filelist)
                xs = np.append(xs,a)
                ys = np.append(ys,b)

        fig.legend(title=t) #Set the fontsize for each label
        #Binning
        binns, inten = felix_binning(xs, ys, delta=DELTA)
        fig.plot(binns, inten, ls='-', marker='', c='k')

        #Exporting the Binned file.
        F = 'OUT/%s.pdf'%(outFilename)
        export_file(F, binns, inten)

        #Set the Xlim values and fontsizes.
        fig.set_xlim([xmin,xmax])
        fig.set_xlabel(r"Calibrated lambda (cm-1)", fontsize=10)
        fig.set_ylabel(r"Normalized Intensity", fontsize=10)
        fig.tick_params(axis='both', which='major', labelsize=majorTickSize)

        #Set the Grid value False if you don't need it.
        fig.grid(True)
        #Set the no. of Minor and Major ticks.
        fig.xaxis.set_minor_locator(MultipleLocator(minor))
        fig.xaxis.set_major_locator(MultipleLocator(major))
        plt.savefig(F)
        if show:
            plt.show()
        plt.close()
        print()
        print("Completed.")
        print()
        
        filesaved()

    except:
        filenotfound()
    return

