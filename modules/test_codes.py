#!/usr/local/bin/python3

from tkinter import *
root = Tk()
root.geometry("400x400")

var = IntVar()
Checkbutton(root, text = "testing", variable = var).pack()
button1 = Button(root, text = "Click", command = lambda: print(var.get())).pack()
root.mainloop()