#!/usr/bin/python3

# Importing modules

# Tkinter modules
from tkinter import Toplevel

# Matplotlb modules
from matplotlib.gridspec import GridSpec as grid

# Built-In Modules
import os

# FELion Modules
from FELion_baseline import Create_Baseline
from FELion_definitions import FELion_Toplevel


def FELion_livePlot(felixfile, location, dpi, parent):
    os.chdir(location)

    ## Embedding figure to tkinter Toplevel
    title_name = 'Baseline-Normline'
    root = Toplevel(parent)
    tk_widget = FELion_Toplevel(root, title_name, location)

    fig, canvas = tk_widget.figure(dpi)
    ax = fig.add_subplot(111)

    ################################ PLOTTING DETAILS ########################################
