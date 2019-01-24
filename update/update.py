

from tkinter import messagebox, Tk
import os, shutil, tempfile, git
from os.path import dirname

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

try:
    # Create temporary dir
    t = tempfile.mkdtemp()

    # Clone into temporary dir
    git.Repo.clone_from('https://github.com/aravindhnivas/FELion-Spectrum-Analyser', t, branch='master', depth=1)

    # Copy desired file from temporary dir
    recursive_overwrite(os.path.join(t, 'modules'), 'C:/FELion-GUI/software')

    # Remove temporary dir
    shutil.rmtree(t)
    ShowInfo("UPDATED", "Program is updated to the latest version.")

except Exception as e:
    ErrorInfo("ERROR: ", e)