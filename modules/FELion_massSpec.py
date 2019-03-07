#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from tkinter import Tk, messagebox

from FELion_definitions import ShowInfo, copy, move, ErrorInfo
from os.path import join, isdir
from matplotlib.widgets import Cursor, RadioButtons

def massSpec(fname, mname, temp, bwidth, ie, location,\
            filelist, avgname, combine, save_fig):

    try:

        plt.rcParams['figure.figsize']=(10,5)
        plt.rcParams['figure.dpi']=100

        os.chdir(location)
        my_path = os.getcwd()

        if not isdir("MassSpec_DATA"):
            os.mkdir("MassSpec_DATA")

        if fname.find(".mass")>0:
            fname = fname.split(".")[0]

        def saveinfo(name):
            if os.path.isfile(my_path+"/MassSpec_DATA/{}.png".format(name)):
                ShowInfo("SAVED", "File %s.png saved \nin MassSpec_DATA directory"%name)
        
        def y_format(label):
                y_fmt = {'log':'log', 'linear': 'linear'}
                fmt = y_fmt[label]
                ax.set_yscale(fmt)
                plt.draw()

        fig, ax = plt.subplots()
        
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
            m_res, m_b0, trap = round(var['res']), int(var['b0']/1000), int(var['trap_time']/1000)
            print(var)

            plt.grid(True)
            ax.plot(x, y, label = '%s: res: %.1f; trap:%ims'%(filename.split('.')[0], m_res, trap))
            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts /{} ms'.format(m_b0))
            plt.title("Filename: {}, for {}, at temp: {}K, and IE(eV): {}"\
                        .format(fname, mname, temp, ie),
                        fontsize = 12)
            ax.set_yscale('log')
            plt.tight_layout()
            plt.legend()

            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
            
            # Choosing btwn liner and log scale
            plt.subplots_adjust(left=0.3)

            axcolor = 'lightgoldenrodyellow'
            rax = plt.axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)
            radio = RadioButtons(rax, ( 'log', 'linear'))
            radio.on_clicked(y_format)

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

                var = {'trap_time': 'm04_ao04_sa_delay', 'res':'m03_ao13_reso', 'q2_float':'m04_ao09_qd2_float', 'b0':'m03_ao09_width'}
                print(var)

                with open(file, 'r') as f:
                    f = np.array(f.readlines())
                for i in f:
                    if not len(i.strip())==0 and i.split()[0]=='#':
                        for j in var:
                            if var[j] in i.split():
                                var[j] = float(i.split()[-3])
                m_res, m_b0, trap = round(var['res']), int(var['b0']/1000), int(var['trap_time']/1000)
                print(var)

                ax.plot(x, y, label = '%s: res: %.1f; trap:%ims, B0:%ims'%(file.split('.')[0], m_res, trap, m_b0))

            plt.grid(True)
            ax.set_xlabel('mass [u]')
            ax.set_ylabel('ion counts')
            plt.grid(True)
            ax.set_title("%s"%avgname, fontsize=12)
            ax.set_yscale('log')
            plt.tight_layout()
            ax.legend()
            
            cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

            # Choosing btwn liner and log scale
            plt.subplots_adjust(left=0.3)
            axcolor = 'lightgoldenrodyellow'
            rax = plt.axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)
            radio = RadioButtons(rax, ( 'log', 'linear'))               
            radio.on_clicked(y_format) 

            if save_fig:
                plt.savefig(join(my_path,"MassSpec_DATA","%s.png"%avgname))
                plt.show()
                saveinfo(avgname)
            else:
                plt.show()
                
    except Exception as e:
        ErrorInfo("ERROR", e)