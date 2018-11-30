#!/usr/bin/python3

from tkinter import *
'''from FELion_avgSpec import avgSpec_plot
from FELion_normline import normline_correction
from f_baseline import f_baseline_correction'''


import FELion_avgSpec, f_baseline, FELion_normline

root = Tk()
root.geometry("500x500")

topFrame = Frame(root, height = 50)
topFrame.pack(fill = "both", expand = False)

frame = Frame(root, bg = "sea green")
frame.pack(fill = "both", expand = True)

content = StringVar()
user_input = Entry(frame, textvariable=content)
content.set("Enter")
user_input.focus()
user_input.pack(pady = 10)

avg = Button(frame, text="avg", command = lambda: FELion_avgSpec.avgSpec_plot())
avg.pack(pady = 10)

norm = Button(frame, text="norm", command = lambda: FELion_normline.normline_correction(user_input.get()))
norm.pack(pady = 10)

base = Button(frame, text = "base", command = lambda: f_baseline.f_baseline_correction(user_input.get()))
base.pack(pady = 10)
root.mainloop()