#!/usr/bin/python3


from tkinter import *
from tkinter import ttk, messagebox
from test_codes import centerIt, framesandlabels

root = Tk()
root.title("FELion Spectrum Analyser")
width_window = 1000
height_window = 400


centerIt(root, width_window, height_window)
framesandlabels(root, "chocolate1", "Test1", "testSub", "chekLeft", "CheckRight")

root.mainloop()