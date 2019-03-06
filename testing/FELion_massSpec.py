#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from tkinter import Tk, messagebox

from FELion_definitions import ShowInfo, copy, move, ErrorInfo
from os.path import join, isdir
from matplotlib.widgets import Cursor

def massSpec(fname, mname, temp, bwidth, ie, location,\
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

        def mass_resolution(filename):
            with open(filename, 'r') as f:
                f = f.readlines()

            res_name = f[-14].split('\t\t')[2].split('#')[-1].strip()
            mass_res = round(float(f[-14].split('\t\t')[3].split('#')[-1].strip()), 2)

            if res_name == 'm03_ao13_reso':
                print('Mass Resolution: %s'%mass_res)
                return mass_res
            else:
                print('ERROR: parameter found here was %s instead of m03_ao13_reso\nPlease adjust the change in script'%res_name)
                return

        if not combine:
            
            filename = fname + ".mass"

            if not os.path.isdir("MassSpec_DATA"):
                os.mkdir("MassSpec_DATA")
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
            else:
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
           
            mass = np.genfromtxt(filename)
            x, y = mass[:,0], mass[:,1]
            m_res = mass_resolution(filename)

            fig, ax = plt.subplots(1)

            plt.grid(True)
            ax.semilogy(x, y, label = '%s: res: %.1f'%(filename.split('.')[0], m_res))
            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts /{} ms'.format(bwidth))
            plt.title("Filename: {}, for {}, at temp: {}K, B0: {}ms and IE(eV): {}"\
                        .format(fname, mname, temp, bwidth, ie))

            plt.tight_layout()
            plt.legend()
            cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

            if save_fig:
                plt.savefig(my_path + "/MassSpec_DATA/{}.png".format(fname))
                plt.show()
                saveinfo(fname)
            else:
                plt.show()

        if combine:
            if filelist == []: 
                return ErrorInfo("Select Files: ", "Click Select File(s)")
            for file in filelist:

                mass = np.genfromtxt(file)
                x, y = mass[:,0], mass[:,1]

                m_res = mass_resolution(file)
                
                plt.grid(True)
                plt.semilogy(x, y, label = '%s: res: %.1f'%(file.split('.')[0], m_res))
            
                plt.legend()

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
                
    except Exception as e:
        ErrorInfo("ERROR", e)