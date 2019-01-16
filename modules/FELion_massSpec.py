#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from tkinter import Tk, messagebox

from FELion_definitions import ShowInfo, copy, move, ErrorInfo

def massSpec(fname, mname, temp, bwidth, ie, xmin, xmax, location,\
            fig_width, fig_height, filelist, avgname, combine, save_fig):

    try:
        os.chdir(location)
        my_path = os.getcwd()
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

            f = open(filename)
            x, y = [],[]
            for i in f:
                if not i[0] == "#" and not i == "\n":
                    a, b = i.split()
                    x.append(float(a))
                    y.append(float(b))
            f.close()
            
            plt.grid(True)
            plt.semilogy(x, y)
            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts /{} ms'.format(bwidth))
            plt.title("Filename: {}, for {}, at temp: {}K, B0: {}ms and IE(eV): {}"\
                        .format(fname, mname, temp, bwidth, ie))
            if save_fig:
                plt.savefig(my_path + "/MassSpec_DATA/{}.png".format(fname))
                plt.show()
                saveinfo(fname)
            else:
                plt.show()

        if combine:
            filelist = filelist.split(",")

            for file in filelist:
                file = file.strip()
                if file.find("mass")>=0:
                    file = file.split(".")[0]
                    
                if len(file) <2:
                    file= fname[0:9] + file +'.mass'
                else:
                    file = file + '.mass'
                f = open(file)
                x, y = [],[]
                for i in f:
                    if not i[0] == "#" and not i == "\n":
                        a, b = i.split()
                        x.append(float(a))
                        y.append(float(b))
                f.close()
                
                plt.grid(True)
                plt.semilogy(x, y, label = file)
            
                plt.legend()

            plt.xlabel('mass [u]')
            plt.ylabel('ion counts /{} ms'.format(bwidth))
            plt.grid(True)
            plt.title("Filename: {}, for {}, at temp: {}K, B0: {}ms and IE(eV): {}".format(fname, mname, temp, bwidth, ie))
            
            if save_fig:
                plt.savefig(my_path + "/MassSpec_DATA/{}.png".format(avgname))
                plt.show()
                saveinfo(avgname)
            else:
                plt.show()
                
    except Exception as e:
        ErrorInfo("ERROR", e)