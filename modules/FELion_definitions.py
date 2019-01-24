#!/usr/bin/python3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import git
import tempfile

# General functions:

copy = lambda pathdir, x: (shutil.copyfile(pathdir + os.sep+ "{}".format(x), pathdir +os.sep+ "DATA"+os.sep+"{}".format(x)), print("%s copied to DATA folder"))
move = lambda pathdir, x: (shutil.move(pathdir +os.sep+ "{}".format(x), pathdir +os.sep+ "DATA"+os.sep+"{}".format(x)), print("%s moved to DATA folder"))

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

# Update modules

def update():
    pass

# Tkinter functions:
####################################

#labels and enty:
class my_label(Frame):
    def __init__(self, parent, label):
        Frame.__init__(self, parent)

        self.label = Label(self, text=label, font = ("Times", 12, "bold"))
        self.label.pack()

class my_entry(Frame):
    def __init__(self, parent, entry):
        Frame.__init__(self, parent)

        self.entry = entry

        if self.entry is int(): self.value = IntVar()
        else: self.value = StringVar()
        
        self.value.set(entry)       
        self.entry = Entry(self, textvariable = self.value, bg = "white",\
                              bd = 5, font = ("Times", 12, "italic"))

        self.entry.pack()

#labels and entry combined:
def labels_and_entry(self, *args, **kwargs):
    label, entry = [i for i in args]
    
    v = {'lx': float(), 'ly': float(), 'ex': float(), 'ey':float(), 'l_rh': 0.05, 'l_rw': 0.1,
                 'e_rw': 0.1, 'e_rh': 0.05}
    
    for i in kwargs:
        if i in v:
            v[i] = kwargs[i]

    self.l1 = my_label(self, label)
    self.l1.place(relx = v['lx'], rely = v['ly'], relheight = v['l_rh'], relwidth = v['l_rw'])

    self.e1 = my_entry(self, entry)
    self.e1.place(relx = v['ex'], rely = v['ey'], relheight = v['e_rh'], relwidth = v['e_rw'])