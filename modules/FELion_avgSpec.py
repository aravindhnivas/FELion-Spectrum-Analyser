#!/usr/bin/python3

## MODULES ##

## Data analysis and plotting packages
import numpy as np
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt

## FELion modules
from FELion_normline import norm_line_felix, felix_binning
from FELion_definitions import ShowInfo, ErrorInfo, move

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
    save, show, DELTA, fileNameList, dpi = args

    def filesaved():
        if os.path.isfile(my_path+"/OUT/{}.pdf".format(outFilename)) and save:
            ShowInfo("SAVED", "File %s.pdf saved"%outFilename)

    try:

        if fileNameList == []:
            return ShowInfo("Information", "Click Select File(s)")

        folders = ["DATA", "EXPORT", "OUT"]
        back_dir = dirname(location)
        
        if set(folders).issubset(os.listdir(back_dir)): 
            os.chdir(back_dir)
            my_path = os.getcwd()
        
        else: 
            os.chdir(location)
            my_path = os.getcwd() 

        for dirs in folders:
            if not isdir(dirs): os.mkdir(dirs)

        figure = plt.figure(figsize=(fwidth, fheight), dpi = dpi)
        fig = figure.add_subplot(1,1,1)
        plt.rcParams['font.size'] = ts
        plt.rcParams['legend.fontsize'] = lgs

        xs = np.array([],dtype='double')
        ys = np.array([],dtype='double')

        foravgshow = True
        normshow = False
        for fname in fileNameList:
            fname = fname.split(".")[0]
            fullname = fname + ".felix"
            basefile = fname + ".base"
            powerfile = fname + ".pow"
            files = [fullname, powerfile, basefile]

            for filenames in files:
                if isfile(filenames): move(my_path, filenames)

            a,b = norm_line_felix(fname, mname, temp, bwidth, ie, save, foravgshow, normshow, dpi)
            fig.plot(a, b, ls='', marker='o', ms=markersz, label=fname)
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

            j ='OUT/%s.png'%(outFilename)
            export_file(F, binns, inten)
            plt.savefig(j)
        
        if show:
            plt.show()
        
        filesaved()
        plt.close()

    except Exception as e:
        ErrorInfo("ERROR", e)