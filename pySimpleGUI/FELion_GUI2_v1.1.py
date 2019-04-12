#!/usr/bin/python3

###############################################################################################
###############################################################################################

# PySimpleGUI
import PySimpleGUI as sg

# Tkinter and matplotlib Modules
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter import Tk, Toplevel, ttk, messagebox, Frame, StringVar, Entry

# DATA Analysis
import numpy as np

# Built-In
import os
from os.path import basename, dirname, isfile, isdir
from glob import glob

###############################################################################################
###############################################################################################

welcome_msg = """

The FELion Spectrum analyser for analysing FELIX data using Python;

It consists: the following functions:
    1. Norm and Avg: For Baseline correction, SpectrumPlot, Average Plot
    2. Mass Spectrum Plot
    3. Powerfile Generator
    4. Plot (For Timescanplot, depletion plot, theory-avg plot and general X,Y plots:)
    5. Update Program (For updating to the latest version from github)

If error: Maybe, try to avoid using //server as the location

The felix datas are saved/moved into "DATA" folder.
The processed raw data output files can be found in "EXPORT".
The processed output files can be found in "OUT".

Report bug/suggestion: aravindh@science.ru.nl

"""

###############################################################################################
# Main Window Layout

class FELion:

    def __init__(self):

        layout = [
            [sg.Text('FELion Spectrum Analyzer', size=(40, 1), justification='center', font='Helvetica 20')],
            [sg.Text(welcome_msg)],
            [sg.Text(' '*20), sg.Button('Mass Spec'), sg.Button('Spectrum'), sg.Button('Powerfile Generator'), sg.Button('Plot'), sg.Text(' '*50), sg.Quit()],
            [sg.Text('')]
        ]

        window = sg.Window('FELion GUI').Layout(layout)
        mass_active = False

        # Event Loop

        while True:

            event, *_ = window.Read(timeout = 100)
            
            if event is None or event == 'Quit':
                break

            if event == 'Mass Spec':
                mass_layout = [
                [sg.Text('Mass Spectrum Analyzer', size=(20, 1), justification='center', font='Helvetica 20')],
                [sg.InputText('Select .mass file', key = 'massfile') , sg.FileBrowse()],
                [sg.Listbox(values=next(os.walk('.'))[1], size=(30, 10), key = 'Folders')],
                [sg.Button('Plot'), sg.Quit()],
                [sg.Text('')]
                ]
                massWindow = sg.Window('Mass Spectrum').Layout(mass_layout)
                massWindow.Finalize()

                mass_active = True

            while mass_active:
                mevent, mvalues = massWindow.Read(timeout = 100)

                if mevent is None or mevent == 'Quit':
                    massWindow.Close()
                    mass_active = False
                
                if mevent == 'Plot':
                    self.massfile = mvalues['massfile']
                    self.mfname = basename(self.massfile)
                    self.mlocatin = dirname(self.massfile)
                    print(f"Filename: {self.mfname}\nLocation: {self.mlocatin}")
                    self.massplot()
                    


    def massplot(self):
        print(os.getcwd())
        
        mass, counts = np.genfromtxt(self.massfile).T

 

felion_gui = FELion()