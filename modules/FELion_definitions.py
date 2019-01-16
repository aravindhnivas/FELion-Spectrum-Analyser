#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os

############
def filenotfound(error, msg):
    root = Tk()
    root.withdraw()
    messagebox.showerror(str(error), str(msg))
    root.destroy()