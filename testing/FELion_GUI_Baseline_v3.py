#!/usr/bin/python3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import shutil
#from FELion_baseline import baseline_correction
from FELion_baseline1 import baseline_correction

from FELion_definitions import update
from os.path import join

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
      app.destroy()

def save_on():
    messagebox.showinfo("FILE SAVED", "File SAVED\nDon't press the Save button again unless different file!")
    app.quit()

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
        Tk.iconbitmap(self,default='C:/FELION-GUI/software/FELion_Icon.ico')
        Tk.wm_title(self, "FELion Baseline Correction v.2.0")
        Tk.wm_geometry(self, "1000x600")

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

        button2 = ttk.Button(self, text="Update Program",
                            command=lambda: update())
        button2.place(relx = x3, rely = y, width = 110, height = height)

        welcome_msg = """
        The FELion Spectrum analyser for analysing FELIX data:

        This program can do Baseline Correction.
        
        Follow the processing with other program "FELion_Normline" for further analysis.

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

        # Opening a Directory:
        self.location = "/"
        self.fname = ""

        def open_dir(self):

            root = Tk()
            root.withdraw()

            root.filename =  filedialog.askopenfilename(initialdir = self.location, title = "Select file", filetypes = (("Felix files","*.felix"),("all files","*.*")))
            filename = root.filename
            filename = filename.split("/")

            self.fname = filename[-1]
            del filename[-1]
            self.location = "/".join(filename)

            root.destroy()
            current_location.config(text = self.location)
            filename_label.config(text = self.fname)
            return
  
        # Labels and buttons:
        browse_loc = ttk.Button(self, text = "Browse File")
        browse_loc.config(command = lambda: open_dir(self))

        # Printing current location:
        current_location = Label(self)
        filename_label = Label(self)
        
        #Label for Entry Box;
        user_input_label = Label(self, text = " Filename:", font=("Times", 10, "bold"))

        #fname, location = open_dir(self)
        #Baseline
        baseline_button = ttk.Button(self, text="Baseline")
        baseline_button.config(command = lambda: baseline_correction(self.fname, self.location, save_check.get()))

        #Save progm button
        #saveButton = ttk.Button(self, text = "click to save")
        #saveButton.config(command = lambda: save_on())

        #SaveAs progm button
        save_check = BooleanVar()
        save_check.set(True)
        save = ttk.Checkbutton(self, text = "Save" ,variable = save_check)
        

        b_diff = 0.2
        b_x1 = 0.1
        b_x2 = b_x1 + b_diff

        y_diff = 0.1
        b_y1 = 0.25
        b_y2 = b_y1 + y_diff
        b_y3 = b_y2 + y_diff + 0.05
        b_y4 = b_y3 + y_diff

        browse_loc.place(relx = b_x1,  rely = b_y1, width = 100, height = 40)
        current_location.place(relx = b_x2,  rely = b_y1, relwidth = 0.6, height = 40)
        filename_label.place(relx = b_x2,  rely = b_y2, relwidth = 0.3, height = 40)

        user_input_label.place(relx = b_x1,  rely = b_y2, width = 100, height = 40)
        baseline_button.place(relx = b_x1,  rely = b_y3, width = 100, height = 40)
        #saveButton.place(relx = b_x2,  rely = b_y3, width = 100, height = 40)
        save.place(relx = b_x2+0.2,  rely = b_y3, width = 100, height = 40)
        #saveAsButton.place(relx = b_x2,  rely = b_y4, width = 100, height = 40)

###################################################################################################################################################
# Main Program

app = FELion_base()

icons_locations = "C:/FELion-GUI/software/"
app.protocol("WM_DELETE_WINDOW", on_closing)

shutdown = PhotoImage(file = join(icons_locations, "power.png"))
restarticon = PhotoImage(file = join(icons_locations, "restart.png"))

power = ttk.Button(app, image=shutdown, text = 'power', command = lambda: app.destroy())
restart = ttk.Button(app, image=restarticon, text = 'restart', command = lambda: os.execl(sys.executable, sys.executable, *sys.argv))

restart.place(relx = 0.95, rely = 0.05)
power.place(relx = 0.95, rely = 0.15)

app.mainloop()