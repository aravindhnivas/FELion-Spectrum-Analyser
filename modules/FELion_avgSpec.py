#!/usr/bin/python3

import numpy as np
import pylab as P
import sys
from os import path
from scipy.optimize import leastsq

from FELion_normline import norm_line_felix
from FELion_normline import felix_binning
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, NullFormatter, NullLocator
import matplotlib.pyplot as plt
from FELion_definitions import *

## modules
import os
from os.path import dirname, isdir, isfile
from tkinter import Tk, messagebox


def export_file(fname, wn, inten):
    f = open(fname.split(".pdf")[0] + '.dat','w')
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
    pwd = os.listdir(my_path + "/DATA") # going into the data folder to fetch all the available data filename.
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
                majorTickSize, outFilename,\
                location, mname, temp, bwidth, ie, save,\
                specificFiles, allFiles, \
                xlabelsz, ylabelsz, fwidth, fheight, markersz, show, DELTA
                ):

    def filesaved():
        if os.path.isfile(my_path+"/OUT/{}.pdf".format(outFilename)) and save:
            ShowInfo("SAVED", "File %s.pdf saved"%outFilename)

         

    try:

        folders = ["DATA", "EXPORT", "OUT", "ToAvg"]
        back_dir = dirname(location)
        
        if set(folders).issubset(os.listdir(back_dir)): 
            os.chdir(back_dir)
            my_path = os.getcwd()
        
        else: 
            os.chdir(location)
            my_path = os.getcwd()
        
        if not isdir("ToAvg"): os.mkdir("ToAvg")

        figure = plt.figure(figsize=(fwidth, fheight), dpi = 100)
        fig = figure.add_subplot(1,1,1)
        plt.rcParams['font.size'] = ts
        plt.rcParams['legend.fontsize'] = lgs

        pwd = os.listdir(os.getcwd()+'/ToAvg')
        f = []
        filesz = lambda x: (os.stat(x).st_size)/1024.0
        for i in pwd:
            if i.find(".felix")>=0:
                f.append(i)
        fileNameList = []
        for i in f:
            if filesz(os.getcwd()+'/ToAvg/'+i)>4.0:
                fileNameList.append(i)

        xs = np.array([],dtype='double')
        ys = np.array([],dtype='double')

        if all and not specificFiles:
            foravgshow = True
            normshow = False
            for filelist in fileNameList:
                a,b = norm_line_felix(filelist, mname, temp, bwidth, ie, save, foravgshow, normshow)
                fig.plot(a, b, ls='', marker='o', ms=markersz, label=filelist)
                xs = np.append(xs,a)
                ys = np.append(ys,b)

        fig.legend(title=t) #Set the fontsize for each label

        #Binning
        binns, inten = felix_binning(xs, ys, delta=DELTA)
        fig.plot(binns, inten, ls='-', marker='', c='k')

        fig.set_xlabel(r"Calibrated lambda (cm-1)", fontsize=xlabelsz)
        fig.set_ylabel(r"Normalized Intensity", fontsize=ylabelsz)
        fig.tick_params(axis='both', which='major', labelsize=majorTickSize)

        fig.grid(True)
        fig.xaxis.set_minor_locator(MultipleLocator(minor))
        fig.xaxis.set_major_locator(MultipleLocator(major))

        if save:
            F = 'OUT/%s.pdf'%(outFilename)
            export_file(F, binns, inten)
            plt.savefig(F)
        
        if show:
            plt.show()
        
        filesaved()
        plt.close()

    except Exception as e:
        ErrorInfo("ERROR", e)