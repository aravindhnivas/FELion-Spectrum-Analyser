from tkinter import *
from tkinter import filedialog
import os

# Opening a Directory:
root = Tk()
root.withdraw()
#root.directory = filedialog.askdirectory()
#root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
filename = root.filename
fname = filename.split("/")[-1]
location = filename
root.destroy()

print(filename)
print(fname)