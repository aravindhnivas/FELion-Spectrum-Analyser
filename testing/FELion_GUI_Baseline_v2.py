#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, messagebox
import os
import shutil


#FELion Module
from FELion_baseline import baseline_correction

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
      root.destroy()

def save_on():
    if messagebox.askokcancel("SAVE","Save the file?"):
        messagebox.showinfo("FILE SAVED", "File SAVED\nDon't press the Save button again unless different file!")
        root.quit()
    return

LARGE_FONT= ("Verdana", 15)

diff = 0.15
x1 = 0.4
x2 = x1 + diff
x3 = x2 + diff
x4 = x3 + diff

y = 0.9
width, height = (100, 40)
smallwidth = 50

class FELion_base(Tk):
    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        Tk.iconbitmap(self,default=os.getcwd()+'/modules/FELion_Icon.ico')
        Tk.wm_title(self, "FELion Baseline Correction v.2.0")
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

        for F in (StartPage_Base, Baseline):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage_Base)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage_Base(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")
        
        label = Label(self, text="Start Page", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        button1 = ttk.Button(self, text="Baseline",
                            command=lambda: controller.show_frame(Baseline))
        button1.place(relx = x1, rely = y, width = width, height = height)

        welcome_msg = """
        The FELion Spectrum analyser for analysing FELIX data:

        This program can do Baseline Correction.
        
        Follow the processing with other program "FELion" for further analysis.

        Report bug/suggestion: aravindh@science.ru.nl
        """
        label = Label(self, text=welcome_msg, justify = "left",\
                font=("Verdana", 11, "italic"), bg="sea green")
        label.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.75)

class Baseline(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")

        label = Label(self, text="Baseline", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        button1 = ttk.Button(self, text="Back to Home",
                        command=lambda: controller.show_frame(StartPage_Base))
        button1.place(relx = x1, rely = y, width = width, height = height)


        # Labels and buttons:

        # Location:
        location_label = Label(self, text = "Location:", font=("Times", 10, "bold"))

        location = StringVar()
        location.set("Enter file lcoation here")
        location_entry = Entry(self, bg = "white", bd = 5,\
                                textvariable=location, justify = LEFT,\
                                font=("Times", 12, "italic"))



        #Label for Entry Box;
        user_input_label = Label(self, text = " Filename:", font=("Times", 10, "bold"))

        #Entry Box;
        init_msg = "Enter here" #initialising message
        content = StringVar()   #defining Stringvar()
        user_input = Entry(self, bg = "white", bd = 5, textvariable=content, justify = LEFT)
        user_input.config(font=("Times", 12, "italic"))
        user_input.focus_set()
        content.set(init_msg)

        #Baseline
        baseline_button = ttk.Button(self, text="Baseline")
        baseline_button.config(command = lambda: baseline_correction(content.get(), location.get()))

        #Save progm button
        saveButton = ttk.Button(self, text = "Save Baseline")
        saveButton.config(command = lambda: save_on())

        b_diff = 0.2
        b_x1 = 0.1
        b_x2 = b_x1 + b_diff

        y_diff = 0.1
        b_y1 = 0.25
        b_y2 = b_y1 + y_diff
        b_y3 = b_y2 + y_diff + 0.05


        location_label.place(relx = b_x1,  rely = b_y1, width = 100, height = 40)
        location_entry.place(relx = b_x2,  rely = b_y1, relwidth = 0.5, height = 40)
        user_input_label.place(relx = b_x1,  rely = b_y2, width = 100, height = 40)
        user_input.place(relx = b_x2,  rely = b_y2, width = 100, height = 40)
        baseline_button.place(relx = b_x1,  rely = b_y3, width = 100, height = 40)
        saveButton.place(relx = b_x2,  rely = b_y3, width = 100, height = 40)


root = FELion_base()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()