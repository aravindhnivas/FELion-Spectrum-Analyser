#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, StringVar, IntVar

LARGE_FONT = 12

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

def labels_and_entry(self, *args, **kwargs):

    label, entry = [i for i in args]

    variables = ['lx', 'ly', 'ex', 'ey', 'l_relheight', 'l_relwidth', 'e_relwidth', 'e_relheight']

    lx, ly, ex, ey = [0.1, 0.2, 0.1, 0.2]
    l_relheight, l_relwidth, e_relwidth, e_relheight = [0.05, 0.1, 0.1, 0.05]

    for i in kwargs:
        if i in variables:
            index = variables.index(i)
            vars()[variables[index]] = kwargs[i]

    self.l1 = my_label(self, label)
    self.l1.place(relx = lx, rely = ly, relheight = l_relheight, relwidth = l_relwidth)

    self.e1 = my_entry(self, entry)
    self.e1.place(relx = ex, rely = ey, relheight = e_relheight, relwidth = e_relwidth)


class FELion(Tk):
    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        Tk.iconbitmap(self,default='C:/FELion-GUI/FELion_Icon.ico')
        Tk.wm_title(self, "FELion-Spectrum Analyser v.2.0")
        Tk.wm_geometry(self, "900x600")
       
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        StatusBarFrame = Frame(self)
        StatusBarFrame.pack(side = "bottom", fill = "both", expand = False)

        statusBar_left_text = "Version 2.0"
        statusBar_left = Label(StatusBarFrame)
        statusBar_left.config(text = statusBar_left_text, \
        relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "w")
        statusBar_left.pack(side = "top", fill = "both", expand = True)

        statusBar_right_text = "Developed at dr. Sandra's Lab FELIX"
        statusBar_right = Label(StatusBarFrame)
        statusBar_right.config(text = statusBar_right_text, \
        relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "e")
        statusBar_right.pack(side = "top", fill = "both", expand = True)

        self.frames = {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")
        
        label = Label(self, text="Start Page", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        labels_and_entry(self,"Filename: ","Molecules")
        labels_and_entry(self, "Temperature: ", 4, ly = 0.2, ey = 0.2, ex = 0.25)

root = FELion()
root.mainloop()