#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from tkinter import Tk, messagebox
from FELion_definitions import ShowInfo, copy, move, ErrorInfo, var_find
from os.path import join, isdir, isfile
from matplotlib.widgets import Cursor

def massSpec(fname, location, mname, temp, bwidth, ie,\
            filelist, avgname, combine, save_fig):

    try:
        os.chdir(location)
        my_path = os.getcwd()

        if not isdir("MassSpec_DATA"):
            os.mkdir("MassSpec_DATA")

        if fname.find(".mass")>=0:
            fname = fname.split(".")[0]

        if not combine:
            filename = fname + ".mass"
            res, b0, trap = var_find(filename, location)

            if not os.path.isdir("MassSpec_DATA"):
                os.mkdir("MassSpec_DATA")
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
            else:
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
           
            mass = np.genfromtxt(filename)
            x, y = mass[:,0], mass[:,1]

            fig, ax = plt.subplots(1)

            plt.grid(True)
            ax.semilogy(x, y, label = f'{fname}: Res: {res}; B0: {b0}; Trap: {trap}')
            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts /{} ms'.format(b0))
            plt.title("Filename: {}, for {}, at temp: {}K, B0: {}ms and IE(eV): {}"\
                        .format(fname, mname, temp, b0, ie))

            plt.tight_layout()
            plt.legend()
            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            if save_fig:
                ShowInfo("SAVED", f"File {fname}.png saved \nin MassSpec_DATA directory")
                plt.savefig(join(my_path, 'MassSpec_DATA', f'{fname}.png'))
                plt.show()
                
            else:
                plt.show()
            
            plt.close()

        if combine:
            if filelist == []: 
                return ErrorInfo("Select Files: ", "Click Select File(s)")

            fig1, ax1 = plt.subplots()

            for file in filelist:
                res, b0, trap = var_find(file, location)

                mass = np.genfromtxt(file)
                x, y = mass[:,0], mass[:,1]
                
                plt.grid(True)
                ax1.semilogy(x, y, label = f'{file}: Res: {res}; B0: {b0}; Trap: {trap}')
                plt.legend()

            cursor = Cursor(ax1, useblit=True, color='red', linewidth=1)

            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts')
            plt.grid(True)
            plt.title(f'{avgname}')
            
            plt.tight_layout()

            if save_fig:
                ShowInfo("SAVED", f"File {avgname}.png saved \nin MassSpec_DATA directory")
                plt.savefig(join(my_path, 'MassSpec_DATA', f'{avgname}.png'))
                plt.show()
            else:
                plt.show()
            plt.close()                
    except Exception as e:
        ErrorInfo("ERROR", e)