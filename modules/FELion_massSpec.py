#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from tkinter import Tk, messagebox


def main(date):
    """  """
    if args.amount:
        for scans in range(args.amount):
            date = input('scan number or filename: ')
            if len(date) <2:
                date= args.date[0:9] + date +'.mass'
            else:
                date= date + '.mass'
            with open(date) as f:
                data = f.read()

            data = data.split('\n')

            x = -np.ones(len(data))
            y = -np.ones(len(data))

            for index, a in enumerate(data):

                if '#' in a or len(a) < 1:
                    if '# m03_ao09_width' in a:
                        a = a.split('\t\t#')
                        b0 = "%.0f" % (int(a[3]) / 1000)
                else:
                    a = a.split('\t')
                    x[index] = float(a[0])
                    y[index] = float(a[1])

            name = f.name[:8].replace('_', '-')

            plt.semilogy(x, y, label= input('legenda input: '))
            plt.legend()

        compound_name = input("What is your compounds name? ")
        compound_structure = input('The structure? ')
        Temp = input('Temperature? ')
        ion = input('Electron energy? ')

        plt.suptitle('Mass spectrum ion source from {} ({}) \n {}, T={}K, B0 opening {} ms, Ee={}V'.format(compound_name, compound_structure, name, Temp, b0, ion))

        plt.xlabel('mass [u]')
        plt.ylabel('ion counts /{} ms'.format(b0))
        plt.grid(True)
        plt.ylim(1)

        plt.show()
    else:
        date= date + '.mass'
        with open(date) as f:
            data = f.read()

        data = data.split('\n')

        x = -np.ones(len(data))
        y = -np.ones(len(data))

        for index, a in enumerate(data):

            if '#' in a or len(a) < 1:
                if '# m03_ao09_width' in a:
                    a = a.split('\t\t#')
                    b0 = "%.0f" % (int(a[3])/1000)
            else:
                a = a.split('\t')
                x[index] = float(a[0])
                y[index] = float(a[1])

        name = f.name[:8].replace('_', '-')

        plt.semilogy(x, y)
        if args.amount:
            plt.title('{}, T={}K, B0 opening {} ms, Ee={}V'.format(name,Temp, b0, ion))
            plt.suptitle('Mass spectrum ion source from {} ({})'.format(compound_name,compound_structure))
        plt.xlabel('mass [u]')
        plt.ylabel('ion counts /{} ms'.format(b0))
        plt.grid(True)
        plt.ylim(1)

        plt.show()

def massSpec(fname, mname, temp, bwidth, ie, xmin, xmax, location,\
            fig_width, fig_height, filelist, avgname, combine, save_fig):

    os.chdir(location)
    my_path = os.getcwd()

    def saveinfo(name):
        if os.path.isfile(my_path+"/MassSpec_DATA/{}.png".format(name)):
            root = Tk()
            root.withdraw()
            messagebox.showinfo("Information", "File '{}.png' SAVED \nin MassSpec_DATA directory"\
                                .format(name))
            root.destroy()


    def filenotfound():
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", "FILE '{}.mass' NOT FOUND".format(fname))
        root.destroy()

    try:
        if fname.find(".mass")>0:
            fname = fname.split(".")[0]

        plt.rcParams['figure.figsize'] = [fig_width,fig_height]
        plt.rcParams['figure.dpi'] = 80
        plt.rcParams['savefig.dpi'] = 100

        if not combine:
            
            filename = fname + ".mass"

            if not os.path.isdir("MassSpec_DATA"):
                os.mkdir("MassSpec_DATA")
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))
            else:
                shutil.copyfile(my_path + "/{}".format(filename), my_path + "/MassSpec_DATA/{}".format(filename))

            with open(filename) as f:
                data = f.read()

            data = data.split('\n')

            x = -np.ones(len(data))
            y = -np.ones(len(data))

            for index, a in enumerate(data):
                if '#' in a or len(a) < 1:
                    if '# m03_ao09_width' in a:
                        a = a.split('\t\t#')
                        b0 = "%.0f" % (int(a[3])/1000)
                else:
                    a = a.split('\t')
                    x[index] = float(a[0])
                    y[index] = float(a[1])
            plt.semilogy(x, y)
            plt.xlabel('Mass [u]')
            plt.ylabel('Ion counts /{} ms'.format(b0))
            plt.grid(True)
            plt.xlim([xmin,xmax])
            plt.ylim(1)
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
                with open(file) as f:
                    data = f.read()

                data = data.split('\n')

                x = -np.ones(len(data))
                y = -np.ones(len(data))

                for index, a in enumerate(data):

                    if '#' in a or len(a) < 1:
                        if '# m03_ao09_width' in a:
                            a = a.split('\t\t#')
                            b0 = "%.0f" % (int(a[3]) / 1000)
                    else:
                        a = a.split('\t')
                        x[index] = float(a[0])
                        y[index] = float(a[1])

                plt.semilogy(x, y, label=file)
                plt.legend()

            plt.xlabel('mass [u]')
            plt.ylabel('ion counts /{} ms'.format(b0))
            plt.grid(True)
            plt.ylim(1)
            plt.xlim([xmin,xmax])
            plt.title("Filename: {}, for {}, at temp: {}K, B0: {}ms and IE(eV): {}".format(fname, mname, temp, bwidth, ie))
            
            if save_fig:
                plt.savefig(my_path + "/MassSpec_DATA/{}.png".format(avgname))
                plt.show()
                saveinfo(avgname)
            else:
                plt.show()
            
    except:
        filenotfound()
