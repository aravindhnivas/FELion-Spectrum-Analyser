from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkfilebrowser import askopenfilenames
import os
from os.path import join

root = Tk()
root.geometry("400x400")

#frame
frame = Frame(root, bg = "sea green")
frame.pack(side = 'top', fill = "both", expand = True)

#label
label = Label(frame, text = "testing")
label.place(relx = 0.1, rely=0.1)

label_test1 = Label(frame, text = 'Filelists: ')
label_test1.place(relx = 0.1, rely = 0.2)

label_test = Label(frame)
label_test.place(relx = 0.1, rely = 0.3)

#button
shutdown = PhotoImage(file = r"D:\FELion-Spectrum-Analyser\testing\power.png")
button = ttk.Button(frame, text = "test Button",image = shutdown, command = lambda: os.execl(sys.executable, sys.executable, *sys.argv))
button.place(relx = 0.3, rely = 0.1)

root.mainloop()