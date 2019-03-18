#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from tkinter import Tk, messagebox

from FELion_definitions import ShowInfo, copy, move, ErrorInfo
from os.path import join, isdir
from matplotlib.widgets import Cursor

def massSpec(fname, location, mname, temp, bwidth, ie,\
            filelist, avgname, combine, save_fig):

    try:
        os.chdir(location)
        my_path = os.getcwd()

        if not isdir("MassSpec_DATA"):
            os.mkdir("MassSpec_DATA")

        if fname.find(".mass")>0:
            fname = fname.split(".")[0]

        def saveinfo(name):
            if os.path.isfile(my_path+"/MassSpec_DATA/{}.png".format(name)):
                ShowInfo("SAVED", "File %s.png saved \nin MassSpec_DATA directory"%name)

        def var_find(fname):
            var = {'res':'m03_ao13_reso', 'b0':'m03_ao09_width', 'trap': 'm04_ao04_sa_delay'}
            print(var)

            with open(fname, 'r') as f:
                f = np.array(f.readlines())
            for i in f:
                if not len(i.strip())==0 and i.split()[0]=='#':
                    for j in var:
                        if var[j] in i.split():
                            var[j] = float(i.split()[-3])

            res, b0, trap = round(var['res']), int(var['b0']/1000), int(var['trap']/1000)
            print(var)
            return res, b0, trap

        if not combine:
            filename = fname + ".mass"
            res, b0, trap = var_find(filename)

            if not os.path.isdir("MassSpec_DATA"):
                os.mkdir("MassSpec_DATA")
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
            else:
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
           
            mass = np.genfromtxt(filename)
            x, y = mass[:,0], mass[:,1]

            fig, ax = plt.subplots(1)

            plt.grid(True)
            ax.semilogy(x, y, label = '%s: Res: %i, B0: %i ms, Trap: %i ms'%(fname, res, b0, trap))
            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts /{} ms'.format(bwidth))
            plt.title("Filename: {}, for {}, at temp: {}K, B0: {}ms and IE(eV): {}"\
                        .format(fname, mname, temp, bwidth, ie))

            plt.tight_layout()
            plt.legend()
            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            if save_fig:
                plt.savefig(my_path + "/MassSpec_DATA/{}.png".format(fname))
                plt.show()
                saveinfo(fname)
            else:
                plt.show()
            
            plt.close()

        if combine:
            if filelist == []: 
                return ErrorInfo("Select Files: ", "Click Select File(s)")

            fig1, ax1 = plt.subplots()

            for file in filelist:
                res, b0, trap = var_find(file)

                mass = np.genfromtxt(file)
                x, y = mass[:,0], mass[:,1]
                
                plt.grid(True)
                ax1.semilogy(x, y, label = '%s: Res: %i, B0: %i ms, Trap: %i ms'%(file.split('.')[0], res, b0, trap))
                plt.legend()

            cursor = Cursor(ax1, useblit=True, color='red', linewidth=1)

            plt.xlabel('mass [u]')
            plt.ylabel('ion counts /{} ms'.format(bwidth))
            plt.grid(True)
            plt.title("%s"%avgname)
            
            plt.tight_layout()

            if save_fig:
                plt.savefig(join(my_path,"MassSpec_DATA","%s.png"%avgname))
                plt.show()
                saveinfo(avgname)
            else:
                plt.show()
            plt.close()
                
    except Exception as e:
        ErrorInfo("ERROR", e)