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

        if not combine:
            
            filename = fname + ".mass"

            if not os.path.isdir("MassSpec_DATA"):
                os.mkdir("MassSpec_DATA")
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
            else:
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
           
            mass = np.genfromtxt(filename)
            x, y = mass[:,0], mass[:,1]

            var = {'trap_time': 'm04_ao04_sa_delay', 'res':'m03_ao13_reso', 'q2_float':'m04_ao09_qd2_float', 'b0':'m03_ao09_width'}
            print(var)

            with open(filename, 'r') as f:
                f = np.array(f.readlines())
            for i in f:
                if not len(i.strip())==0 and i.split()[0]=='#':
                    for j in var:
                        if var[j] in i.split():
                            var[j] = float(i.split()[-3])
            m_res, m_b0 = round(var['res']), int(var['b0']/1000)

            print(var)

            fig, ax = plt.subplots(1)

            plt.grid(True)
            ax.semilogy(x, y, label = '%s: res: %.1f'%(filename.split('.')[0], m_res))
            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts /{} ms'.format(m_b0))
            plt.title("Filename: {}, for {}, at temp: {}K, B0: {}ms and IE(eV): {}"\
                        .format(fname, mname, temp, m_b0, ie))

            plt.tight_layout()
            plt.legend()

            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            if save_fig:
                plt.savefig(my_path + "/MassSpec_DATA/{}.png".format(fname))
                plt.show()
                saveinfo(fname)
            else:
                plt.show()

        if combine:
            
            fig, ax = plt.subplots(1)

            if filelist == []: 
                return ErrorInfo("Select Files: ", "Click Select File(s)")
            for file in filelist:

                mass = np.genfromtxt(file)
                x, y = mass[:,0], mass[:,1]

                m_res = mass_resolution(file)
                
                plt.grid(True)
                ax.semilogy(x, y, label = '%s: res: %.1f'%(file.split('.')[0], m_res))
            
                plt.legend()
            plt.xlabel('mass [u]')
            plt.ylabel('ion counts /{} ms'.format(bwidth))
            plt.grid(True)
            plt.title("%s"%avgname)
            plt.tight_layout()
            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            if save_fig:
                plt.savefig(join(my_path,"MassSpec_DATA","%s.png"%avgname))
                plt.show()
                saveinfo(avgname)
            else:
                plt.show()
                
    except Exception as e:
        ErrorInfo("ERROR", e)