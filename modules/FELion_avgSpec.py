#!/usr/bin/python3

## MODULES ##

# Data analysis and plotting packages
import numpy as np

# Matplotlib Modules
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt

# Tkinter Modules
from tkinter import Toplevel

# FELion modules
from FELion_normline import norm_line_felix, felix_binning
from FELion_definitions import ShowInfo, ErrorInfo, move, FELion_Toplevel, FELion_widgets

# Built-in Modules
import os
from os.path import dirname, isdir, isfile

# Error traceback
import traceback


def avgSpec_plot(*args):

    t, ts, lgs, minor, major, majorTickSize, markersz,\
        xlabelsz, ylabelsz, fwidth, fheight, outFilename,\
        location, mname, temp, bwidth, ie,\
        DELTA, fileNameList, dpi, parent, hd = args

    try:

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
            if not isdir(dirs):
                os.mkdir(dirs)

        xs = np.array([], dtype='double')
        ys = np.array([], dtype='double')

        foravgshow = True
        if not hd:

            # Embedding figure to tkinter Toplevel
            title_name = 'Average Spectrum'
            root = Toplevel(parent)
            tk_widget = FELion_Toplevel(
                root, title_name, location, add_buttons=False)

            fig, canvas = tk_widget.figure(dpi, figsize=(fwidth, fheight))
            ax = fig.add_subplot(111)
            frame = tk_widget.get_widget_frame()

            widget = FELion_widgets(frame)
            save_name = widget.entries(
                'Entry', outFilename, 0.1, 0.1, bd=5, relwidth=0.5, relheight=0.05)

            for f in fileNameList:
                felixfile = f
                fname = f.split(".")[0]
                basefile = fname + ".base"
                powerfile = fname + ".pow"
                files = [felixfile, powerfile, basefile]

                for filenames in files:
                    if isfile(filenames):
                        move(my_path, filenames)

                print(f'\nFilename: {felixfile}\n')
                a, b = norm_line_felix(
                    felixfile, mname, temp, bwidth, ie, foravgshow, location, dpi, parent)
                ax.plot(a, b, ls='', marker='o', ms=markersz, label=felixfile)
                xs = np.append(xs, a)
                ys = np.append(ys, b)

            # Binning
            binns, inten = felix_binning(xs, ys, delta=DELTA)
            ax.plot(binns, inten, ls='-', marker='', c='k')

            ax.set_xlabel(r"Calibrated lambda $(cm^-1)$", fontsize=xlabelsz)
            ax.set_ylabel(r"Normalized Intensity", fontsize=ylabelsz)
            ax.set_title('$%s$'%t, fontsize=ts)

            ax.tick_params(axis='both', which='major', labelsize=majorTickSize)
            ax.grid(True)
            ax.xaxis.set_minor_locator(MultipleLocator(minor))
            ax.xaxis.set_major_locator(MultipleLocator(major))

            l = ax.legend(fontsize=lgs)
            #l.get_title().set_fontsize()

            def save():
                # Save figure as .pdf
                F = f'./OUT/{save_name.get()}.pdf'
                fig.savefig(F)
                print(f'File {F} saved in /OUT Directory\n')

                # Export File as .dat
                with open(f'./EXPORT/{save_name.get()}.dat', 'w') as f:
                    f.write(
                        f"#DATA points as shown in figure: {save_name.get()}.pdf file!\n")
                    f.write("#wn (cm-1)       intensity\n")
                    for i in range(len(binns)):
                        f.write("{:8.3f}\t{:8.2f}\n".format(binns[i], inten[i]))

                print(f'File {save_name.get()}.dat saved in /EXPORT Directory')

                ShowInfo(
                    'Saved', f'File {save_name.get()}.pdf saved in /OUT Directory\nFile {save_name.get()}.dat saved in /EXPORT Directory')

            widget.buttons('Save', 0.1, 0.2, save, relwidth=0.5, relheight=0.05)
            canvas.draw()

        if hd:

            with plt.style.context(['science', 'scatter']):
                fig, ax = plt.subplots()

                for f in fileNameList:
                    felixfile = f
                    fname = f.split(".")[0]
                    basefile = fname + ".base"
                    powerfile = fname + ".pow"
                    files = [felixfile, powerfile, basefile]

                    for filenames in files:
                        if isfile(filenames):
                            move(my_path, filenames)

                    print(f'\nFilename: {felixfile}\n')
                    a, b = norm_line_felix(
                        felixfile, mname, temp, bwidth, ie, foravgshow, location, dpi, parent)
                    ax.plot(a, b, ms=0.5, label=felixfile.replace('_', '/'))
                    xs = np.append(xs, a)
                    ys = np.append(ys, b)

                # Binning
                binns, inten = felix_binning(xs, ys, delta=DELTA)
                ax.plot(binns, inten, 'k-', label='$\Delta$=%i'%DELTA)

                # labels and title
                ax.set(xlabel='Wavenumber $(cm^-1)$', ylabel='Intensity', title='$%s$'%t)
                ax.legend(fontsize=6)

                if not isdir('./OUT'): os.mkdir('./OUT')

                fig.savefig(f'./OUT/{outFilename}_high_res.pdf')
                fig.savefig(f'./OUT/{outFilename}_high_res.png', dpi=dpi*3)

                if isfile(f'./OUT/{outFilename}_high_res.pdf') and isfile(f'./OUT/{outFilename}_high_res.png'):
                    print(f'File saved: {outFilename}_high_res.pdf and {outFilename}_high_res.png\nLocation: {location}')
                    ShowInfo('Saved', f'{outFilename}_high_res.pdf and {outFilename}_high_res.png saved.\nLocation: {location}')

    except:
        ErrorInfo('Error: ', traceback.format_exc())