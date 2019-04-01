#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilenames, askopenfilename, askdirectory
import os, shutil, tempfile, git, subprocess, sys
from os.path import isdir, dirname, join, isfile

import datetime
import numpy as np

# General functions:
copy = lambda pathdir, x: (shutil.copyfile(join(pathdir, x), join(pathdir,"DATA" ,x)), print("%s copied to DATA folder" %x))
move = lambda pathdir, x: (shutil.move(join(pathdir, x), join(pathdir,"DATA" ,x)), print("%s moved to DATA folder"%x))

colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

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


# Normline Filecheck method

def filecheck(my_path, basefile, powerfile, fullname):
    
    #File check
    if not isfile(join(my_path, "DATA", fullname)):
        if isfile(join(my_path, fullname)):
            move(my_path, fullname)
        else:
            return ErrorInfo("ERROR: ", "File %s NOT found"%fullname)

    #Powefile check
    if not isfile(join(my_path, "DATA", powerfile)):
        if isfile(join(my_path, 'Pow', powerfile)):
            shutil.move(join(my_path, "Pow", powerfile), join(my_path,"DATA"))

        elif isfile(join(my_path, powerfile)):
            move(my_path, powerfile)
        
        else:
            return ErrorInfo("ERROR: ", "Powerfile: %s NOT found"%powerfile)

    #Basefile check
    if not isfile(join(my_path, "DATA", basefile)):
        if isfile(join(my_path, basefile)):
            move(my_path, basefile)
        else:
            return ErrorInfo("ERROR: ", "Basefile: %s NOT found"%basefile)

    return True

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
    'bg':'white',
    'bd':0,
    'anchor':'w',
    'relief':SOLID,
    'relwidth': 0.1,
    'relheight': 0.06,
    'justify': 'left',
    'label': '',
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
LARGE_FONT= ("Verdana", 15)

#################### Definitions #############################
def var_check(kw):
    for i in constants:
        if not i in list(kw.keys()):
            kw[i] = constants[i]
    return kw

def outFile(fname, location, file):
    try:
        os.chdir(location)
        my_path = os.getcwd()

        def saveinfo():
                os.chdir(location)
                if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                        ShowInfo("SAVED", "File %s.pow saved in /Pow directory"%fname)
 
        def write():
                f = open(my_path+"/Pow/{}.pow".format(fname), "w")
                f.write(file)
                f.close()
                saveinfo()

        if not os.path.isdir("Pow"): os.mkdir("Pow") 

        if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                messagebox.showerror("OVERWRITE","File already exist")
                if messagebox.askokcancel("OVERWRITE", \
                        "Do yo want to overwrite the existing {}.pow file?".format(fname)):
                        write()
                        
        else:
                write()

    except Exception as e:
            ErrorInfo("ERROR", e)

def var_find(fname, location):
    print(f'###############\nFile: {fname}\nLocation: {location}\n###############')

    if not fname is '':
        os.chdir(location)
        var = {'res':'m03_ao13_reso', 'b0':'m03_ao09_width', 'trap': 'm04_ao04_sa_delay'}
        print(var)

        with open(fname, 'r') as f:
            f = np.array(f.readlines())
        for i in f:
            if not len(i.strip())==0 and i.split()[0]=='#':
                for j in var:
                    if var[j] in i.split():
                        var[j] = float(i.split()[-3])

        res, b0, trap = round(var['res'], 1), int(var['b0']/1000), int(var['trap']/1000)
        print(var)

        return res, b0, trap
    else:
        return 0, 0, 0
##############################################################
class FELion_widgets(Frame):
    
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent)
        self.parent = parent
        self.location = "/"
        self.fname = ""
        self.filelist = []

        if 'cnt' in kw:
            self.cnt = kw['cnt']
              
    def labels(self, *args, **kw):
        txt = args[0]
        x, y = args[1], args[2]
        kw = var_check(kw)
        
        self.parent.txt = Label(self.parent, text = txt, justify = kw['justify'], font = kw['font'], bg = kw['bg'], bd = kw['bd'], relief = kw['relief'])
        self.parent.txt.place(relx = x, rely = y, anchor = kw['anchor'], relwidth = kw['relwidth'], relheight = kw['relheight'])

        if 'help' in kw:
            on_enter = lambda x: self.cnt.statusBar_left.config(text = kw['help'])
            on_leave = lambda x: self.cnt.statusBar_left.config(text = self.cnt.statusBar_left_text)

            self.parent.txt.bind('<Enter>', on_enter)
            self.parent.txt.bind('<Leave>', on_leave)

        return self.parent.txt

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
        
        self.button.place(relx = x, rely = y, relwidth = kw['relwidth'], relheight = kw['relheight'])

        if 'help' in kw:
            on_enter = lambda x: self.cnt.statusBar_left.config(text = kw['help'])
            on_leave = lambda x: self.cnt.statusBar_left.config(text = self.cnt.statusBar_left_text)

            self.button.bind('<Enter>', on_enter)
            self.button.bind('<Leave>', on_leave)

    def entries(self, method,  *args, **kw):
        txt, x, y = args[0], args[1], args[2]
        kw = var_check(kw)
        
        if method == 'Entry':
            if isinstance(txt, str): self.parent.txt = StringVar()
            elif isinstance(txt, int) or isinstance(txt, float): self.parent.txt = DoubleVar()
                
            self.parent.txt.set(txt)
            self.parent.entry = Entry(self.parent, bg = kw['bg'], bd = kw['bd'], textvariable = self.parent.txt, font = kw['font'])
            self.parent.entry.place(relx = x, rely = y, anchor = kw['anchor'], relwidth = kw['relwidth'], relheight = kw['relheight'])
            
            if 'help' in kw:
                on_enter = lambda x: self.cnt.statusBar_left.config(text = kw['help'])
                on_leave = lambda x: self.cnt.statusBar_left.config(text = self.cnt.statusBar_left_text)

                self.parent.entry.bind('<Enter>', on_enter)
                self.parent.entry.bind('<Leave>', on_leave)
            
            
            return self.parent.txt

        elif method == 'Check':
            self.parent.txt = BooleanVar()
            if 'default' in kw: self.parent.txt.set(kw['default'])
            else: self.parent.txt.set(False)

            self.parent.Check = ttk.Checkbutton(self.parent, text = txt, variable = self.parent.txt)
            self.parent.Check.place(relx = x, rely = y, relwidth = kw['relwidth'], relheight = kw['relheight'])

            if 'help' in kw:
                on_enter = lambda x: self.cnt.statusBar_left.config(text = kw['help'])
                on_leave = lambda x: self.cnt.statusBar_left.config(text = self.cnt.statusBar_left_text)

                self.parent.Check.bind('<Enter>', on_enter)
                self.parent.Check.bind('<Leave>', on_leave)

            return self.parent.txt
        
        elif method == 'power_box':
            self.parent.T = Text(self.parent)
            self.parent.S = Scrollbar(self.parent)
            self.parent.T.config(yscrollcommand = self.parent.S.set)
            self.parent.S.config(command = self.parent.T.yview)
            
            self.parent.T.insert(END, txt)

            self.parent.T.place(relx = x,  rely = y, relwidth = 0.7, relheight = 0.4)
            self.parent.S.place(relx = x + 0.7,  rely = y, width = 15, relheight = 0.4)

            return self.parent.T

    def open_dir(self, file_type):
        root = Tk()
        root.withdraw()

        root.filename =  askopenfilename(initialdir = self.location, title = "Select file", filetypes = (file_type, ("all files","*.*")))
        filename = root.filename
        filename = filename.split("/")

        self.full_name = root.filename

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

    def open_full_dir(self):
        root = Tk()
        root.withdraw()
        root.directory =  askdirectory()
        self.location = root.directory
        root.destroy()
        return self.location        