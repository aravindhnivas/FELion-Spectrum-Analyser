#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilenames, askopenfilename
import os, shutil, tempfile, git, subprocess, sys
from os.path import isdir, dirname, join
from tempfile import TemporaryDirectory

# General functions:
copy = lambda pathdir, x: (shutil.copyfile(join(pathdir, x), join(pathdir,"DATA" ,x)), print("%s copied to DATA folder" %x))
move = lambda pathdir, x: (shutil.move(join(pathdir, x), join(pathdir,"DATA" ,x)), print("%s moved to DATA folder"%x))

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

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def update(*args):
    try:
        t = "C:/FELion_update_cache"
        git.Repo.clone_from('https://github.com/aravindhnivas/FELion-Spectrum-Analyser', t, branch='master', depth=1)
        recursive_overwrite(os.path.join(t, 'modules'), 'C:/FELion-GUI/software')
        ShowInfo("UPDATED", "Program is updated to the latest version.\nPlease restart the program.")

    except Exception as e:
        ErrorInfo("ERROR: ", e)

#################################################################################
############################### Tkinter functions ###############################

#################### constants ###############################
constants = {

    'width':50,
    'height':50,
    'font':("Verdana", 10, "italic"),
    'bg':'sea green',
    'bd':0,
    'anchor':'w',
    'relief':SOLID,
    'relwidth': 0.1,
    'relheight': 0.06,
    'justify': 'left',

}

welcome_msg = """
The FELion Spectrum analyser for analysing FELIX data using Python;

It consists: the following functions:
    1. Normline and Average Spectrum Plot
    2. Mass Spectrum Plot
    3. Powerfile Generator
    4. Plot (For general X,Y plots:)
    5. Update Program (For updating to the latest version from github)

NOTE: Before using Normline and Average Spectrum plot functions: 
Make sure you already did "Baseline Correction" using "FELion_Baseline" Program

If error: Maybe, try to avoid using //server as the location

The processed raw data output files can be found in "EXPORT" and "DATA" folder.
The processed output files can be found in "OUT" and "MassSpec_DATA"

Report bug/suggestion: aravindh@science.ru.nl
"""

#################### Variables ###############################

felix_files_type = ("Felix Files", "*.felix")
mass_files_type = ("Mass Files", "*.mass")
time_files_type = ("Timescan Files", "*.scan")
pow_files_type = ("Pow Files", "*.pow")
all_files_type = ("All files", "*")


#################### Definitions #############################

def var_check(kw):
    for i in constants:
        if not i in list(kw.keys()):
            kw[i] = constants[i]
    return kw
    
##############################################################

class Entry_widgets(Frame):
    
    def __init__(self, parent, method,  *args, **kw):
        Frame.__init__(self, parent)
        self.parent = parent
        self.txt, x, y = args[0], args[1], args[2]
        kw = var_check(kw)
        
        if method == 'Entry':
            if isinstance(self.txt, str): self.value = StringVar()
            elif isinstance(self.txt, int): self.value = IntVar()
            elif isinstance(self.txt, tuple): self.value = StringVar()
                
            self.value.set(self.txt)
            self.entry = Entry(self.parent, bg = kw['bg'], bd = kw['bd'], textvariable = self.value, font = kw['font'])

            if 'relwidth' in kw:
                self.entry.place(relx = x, rely = y, anchor = kw['anchor'], relwidth = kw['relwidth'], relheight = kw['relheight'])
            else:
                self.entry.place(relx = x, rely = y, anchor = kw['anchor'], width = kw['width'], height = kw['height'])
                
        elif method == 'Check':
            self.value = BooleanVar()
            if 'default' in kw: self.value.set(kw['default'])
            else: self.value.set(False)

            self.Check = ttk.Checkbutton(self.parent, text = self.txt, variable = self.value)

            if 'relwidth' in kw:
                self.Check.place(relx = x, rely = y, relwidth = kw['relwidth'], relheight = kw['relheight'])
            else:
                self.Check.place(relx = x, rely = y, width = kw['width'], height = kw['height'])
     
    def get(self):
        return self.value.get()

class FELion_widgets(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        ## Initial parameters:
        self.parent = parent
        self.location = "/"
        self.fname = ""
        self.filelist = []
              
    def labels(self, *args, **kw):
        self.txt = args[0]
        x, y = args[1], args[2]
        kw = var_check(kw)
        
        self.label = Label(self.parent, text = self.txt, justify = kw['justify'], font = kw['font'], bg = kw['bg'], bd = kw['bd'], relief = kw['relief'])
        if 'relwidth' in kw:
            self.label.place(relx = x, rely = y, anchor = kw['anchor'], relwidth = kw['relwidth'], relheight = kw['relheight'])
        else:
            self.label.place(relx = x, rely = y, anchor = kw['anchor'], width = kw['width'], height = kw['height'])
    
    def buttons(self, *args, **kw):
        btn_txt = args[0]
        x, y = args[1], args[2]
        func = args[3]
        
        kw = var_check(kw)
        
        if len(args)>4:
            func_parameters = args[4:]
            self.button = ttk.Button(self.parent, text = btn_txt, command = lambda: func(*func_parameters))
        else: 
            self.button = ttk.Button(self.parent, text = btn_txt, command = lambda: func())  
        if 'relwidth' in kw:
            self.button.place(relx = x, rely = y, relwidth = kw['relwidth'], relheight = kw['relheight'])
        else:
            self.button.place(relx = x, rely = y, width = kw['width'], height = kw['height'])

    def open_dir(self, file_type):
        root = Tk()
        root.withdraw()

        root.filename =  askopenfilename(initialdir = self.location, title = "Select file", filetypes = (file_type, ("all files","*.*")))
        filename = root.filename
        filename = filename.split("/")

        self.fname = filename[-1]
        del filename[-1]
        
        self.location = "/".join(filename)
        root.destroy()
        
        return self.fname, self.location

    def openfilelist(self, file_type):
        self.filelist = [] # to prevent appending previously selected files
        self.openlist = askopenfilenames(initialdir=self.location, initialfile='tmp',
                        filetypes=[file_type, ("All files", "*")])

        for i in self.openlist:
            location = i.split("/")
            file = location[-1]
            self.filelist.append(file)
            del location[-1]
            self.location = "/".join(location)

        return self.filelist, self.location