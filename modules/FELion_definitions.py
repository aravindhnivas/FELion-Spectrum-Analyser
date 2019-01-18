#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import shutil


# General functions:

copy = lambda pathdir, x: (shutil.copyfile(pathdir + "/{}".format(x), pathdir + "/DATA/{}".format(x)), print("%s copied to DATA folder"))
move = lambda pathdir, x: (shutil.move(pathdir + "/{}".format(x), pathdir + "/DATA/{}".format(x)), print("%s moved to DATA folder"))

# Tkinter messagebox

def ErrorInfo(error, msg):
    root = Tk()
    root.withdraw()
    messagebox.showerror(str(error), str(msg))
    root.destroy()

def ShowInfo(info, msg):
    root = Tk()
    root.withdraw()
    messagebox.showinfo(str(info), str(msg))
    root.destroy()

# Tkinter functions:
####################################

#browse files and display it's location and file selected
width, height = 50, 100

class tkinter_func(Frame):
    def __init__(self, txt):
        Frame.__init__(self, bg="sea green")
        self.txt = txt

    def labels(self):
        label = Label(self, text=self.txt, \
                font=12, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)