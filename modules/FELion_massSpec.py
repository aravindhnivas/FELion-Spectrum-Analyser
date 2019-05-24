#!/usr/bin/python3

# MODULES

# Data analysis and visualisation Modules
import numpy as np

# matplotlib modules
from matplotlib.widgets import Cursor
from matplotlib.ticker import MultipleLocator
from matplotlib import style
import matplotlib.pyplot as plt

# Tkinter Modules
from tkinter import Toplevel
from tkinter.messagebox import askokcancel

# Built-In Modules
import os
import shutil
from os.path import join, isdir, isfile
from pathlib import Path as pt
from time import time as check_time
#from pathlib import Path as pt

# FELion Definitions
from FELion_definitions import ShowInfo, ErrorInfo, var_find, FELion_Toplevel, FELion_widgets

# Error traceback
import traceback


class massSpec:

    def __init__(self, *args):

        self.t, self.ts, self.lgs, self.minor, self.major, self.majorTickSize, \
            self.xlabelsz, self.ylabelsz, self.fwidth, self.fheight, self.avgname,\
            self.location, self.mname, self.temp, self.ie,\
            self.combine, self.massfile, self.filelist, self.dpi, self.parent = args

        self.mname = '$%s$'%self.mname
        
        os.chdir(self.location)
        if not isdir('./OUT'):
            os.mkdir('./OUT')

        try:
            if not self.combine:
                if not self.massfile.endswith('.mass'):
                    ErrorInfo('Not a .mass file', 'Please select a .mass file')

                print(f'\nSingle Mode:\nMassfile: {self.massfile}\n')
                self.mass_plot()

            if self.combine:
                if len(self.filelist) < 1:
                    ErrorInfo("Select Files: ", "Click Select File(s)")

                print(f'\Combine Mode:\nMassfiles: {self.filelist}\n')
                self.mass_plot()

        except:
            ErrorInfo('Error: ', traceback.format_exc())

    def open_mass_file(self, filename):
        print(f'\nOpening Massfile to plot: {filename}\n')
        res, b0, trap = var_find(filename, self.location)
        mass, counts = np.genfromtxt(filename).T

        return res, b0, trap, mass, counts

    def mass_plot(self):

        # Making figure, canvas and ax
        self.embbed_tkinter()

        if self.combine:
            files = self.filelist
        else:
            files = [self.massfile]

        for file in files:
            res, b0, trap, mass, counts = self.open_mass_file(file)
            fname = file.split('.')[0]

            self.ax.semilogy(
                mass, counts, label=f'{fname}: Res: {res}; B0: {b0}ms; Trap: {trap}ms')

        # Configuring title
        if not self.combine or len(self.filelist) == 1:
            self.res, self.b0, self.trap, self.mass, self.counts = res, b0, trap, mass, counts
            self.fname = fname
            self.ax.set_title(
                f'{self.fname} for {self.mname} at {self.temp}K with IE:{self.ie}eV')
        else:
            self.ax.set_title(f'{self.avgname}')

        # Configuring figure
        self.ax.grid(True)
        self.ax.set_xlabel('Mass [u]', fontsize=self.xlabelsz)
        self.ax.set_ylabel(f'Ion counts', fontsize=self.ylabelsz)
        l = self.ax.legend(title=self.t, fontsize=self.lgs)
        l.get_title().set_fontsize(self.ts)
        self.ax.xaxis.set_minor_locator(MultipleLocator(self.minor))
        self.ax.xaxis.set_major_locator(MultipleLocator(self.major))
        self.ax.tick_params(axis='both', which='major',
                            labelsize=self.majorTickSize)

        cursor = Cursor(self.ax, useblit=True, color='red', linewidth=1)
        self.canvas.draw()

    def embbed_tkinter(self):

        ####################################### Tkinter figure #######################################

        # Embedding figure to tkinter Toplevel
        if self.combine:
            title_name = f'Mass Spec: Combine Mode active'
        else:
            title_name = f'Mass Spec: {self.massfile}: Single Mode active'

        root = Toplevel(self.parent)
        tk_widget = FELion_Toplevel(
            root, title_name, self.location, add_buttons=False)

        # Making frames
        frame = tk_widget.get_widget_frame()
        self.widget = FELion_widgets(frame)

        # Making figure
        self.fig, self.canvas = tk_widget.figure(
            self.dpi, figsize=(self.fwidth, self.fheight))
        self.ax = self.fig.add_subplot(111)

        # Making widgets in tkinter frame
        self.masspec_widgets()

    def masspec_widgets(self):

        self.save_name = self.widget.entries(
            'Entry', 'Plot', 0.1, 0.05, relwidth=0.5, relheight=0.05, bd=5)
        save_btn = self.widget.buttons('Save', 0.1, 0.1, self.save,
                                       relwidth=0.5, relheight=0.05)

        self.log = self.widget.entries('Check', 'Log', 0.1, 0.2,
                                       relwidth=0.5, relheight=0.05, default=True)
        update_btn = self.widget.buttons(
            'Update Plot', 0.1, 0.3, self.update, relwidth=0.5, relheight=0.05)

        high_res = self.widget.buttons('Publication Quality\n(HD-LATEX)',
                                       0.1, 0.37, self.publication, relwidth=0.7, relheight=0.07)

        self.warning_label = self.widget.labels(
            'CAUTION!\nRendering will be slow', 0.1, 0.5, bg='grey', relwidth=0.8, relheight=0.07)

        self.render_info = self.widget.labels(
            '', 0.1, 0.6, bg='light grey', relwidth=0.75, relheight=0.07)

    def save_info(self):
        self.fig.savefig(f'./OUT/{self.save_name.get()}.png')
        ShowInfo(
            'SAVED', f'File: {self.save_name.get()}.png saved in OUT/ directory.')
        print(
            f'Filename saved: {self.save_name.get()}.png\nLocation: {self.location}\n')

    def save(self):
        print('Saving Plot\n')

        if isfile(f'./OUT/{self.save_name.get()}.png'):
            if askokcancel('Overwrite?', f'File: {self.save_name.get()}.png already present. \nDo you want to Overwrite the file?'):
                self.save_info()
        else:
            self.save_info()

    def log_check(self, ax, canvas, sci=True):

        if self.log.get():
            ax.set_yscale('log')
        else:
            ax.set_yscale('linear')
            if sci:
                ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        canvas.draw()

    def update(self):

        print('Updating Plot\n')
        t0 = check_time()

        self.log_check(self.ax, self.canvas)

        t1 = check_time()
        time_log = (t1-t0)*100

        print(f'Redrawn in {time_log:.2f} ms\n')

    def publication(self):

        self.render_info.config(text="Please Wait\nRendering", bg='light blue')

        try:
            t0 = check_time()
            print('\nHigh Resolution image rendering\n')

            with plt.style.context(['science']):

                plt_fig, plt_ax = plt.subplots(dpi=self.dpi*3)

                if not self.combine or len(self.filelist) == 1:
                    plt_ax.plot(self.mass, self.counts, label='$%s$' %
                                self.fname.replace('_', '/'))
                    title = f'Res: {self.res}; Trap: {self.trap}ms; T: {self.temp}K; IE :{self.ie}eV'
                    plt_ax.set_title('$%s$' % title)
                    l0 = plt_ax.legend(title='$%s$' %
                                       self.mname, fontsize=self.lgs)
                    l0.get_title().set_fontsize(self.ts)

                elif self.combine and len(self.filelist) > 1:
                    for file in self.filelist:

                        res, b0, trap, mass, counts = self.open_mass_file(file)
                        fname = file.split('.')[0].replace('_', '/')

                        lg = f'{fname}: Res: {res}; Trap: {trap}ms; T: {self.temp}K; B0: {b0}ms; IE :{self.ie}eV'
                        plt_ax.plot(mass, counts, label='$%s$' % lg)

                        plt_ax.set_title('$%s$'%self.mname)
                        l1 = plt_ax.legend(fontsize=self.lgs-6)
                        # l1.get_title().set_fontsize(self.ts-6)

                self.log_check(plt_ax, plt_fig.canvas, sci=False)

                # Configuring plot
                plt_ax.set_xlabel('Mass [u]')
                plt_ax.set_ylabel('Counts')

                plt_fig.savefig(f'./OUT/{self.save_name.get()}_high_res.pdf')
                plt_fig.savefig(
                    f'./OUT/{self.save_name.get()}_high_res.png', dpi=self.dpi*3)

                t1 = check_time()
                time_log = (t1-t0)*100

                print(f'Rendered in {time_log:.2f} ms\n')
                print(
                    f'File saved: {self.save_name.get()}_high_res.png\nLocation: {self.location}')

                self.render_info.config(text="Completed/Saved", bg='green')

        except:

            self.render_info.config(text="ERROR!!", bg='red')

            print(f'ERROR: {traceback.format_exc()}\n')
            ErrorInfo('Error: ', traceback.format_exc())
