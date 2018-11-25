## A simple GUI program for FELion Instrument:

from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# User defined definitions:
def on_closing():
  if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.destroy()



#Main configuration:
###########################################################################################
###########################################################################################
root = Tk()

#Defining the main window's dimensions:
width_window = 700
height_window = 500

#Making window appear at the center of your computer screen:
your_computer_screen_width = root.winfo_screenwidth()
your_computer_screen_height = root.winfo_screenheight()
x_coordinate = (your_computer_screen_width/2) - (width_window/2)
y_coordinate = (your_computer_screen_height/2) - (height_window/2)
root.geometry("%dx%d+%d+%d" %(width_window, height_window, x_coordinate, y_coordinate))

#Defining the window titile
root.title("FELion Spectrum Analyser")

#Configuring window
root.config()

###########################################################################################
###########################################################################################

#Frames:
###########################################################################################
###########################################################################################

#top frames:
height_topFrame = 100
topFrame = Frame(root)
topFrame.config(height = height_topFrame)
topFrame.pack(side = "top", fill = "both", expand = False)
topFrame.grid_rowconfigure(0, weight = 1)
topFrame.grid_columnconfigure(0, weight = 1)

#bottom frames
bottomFrame = Frame(root)
bottomFrame.config(bg = "white")
bottomFrame.pack(side = "top", fill = "both", expand = True)
bottomFrame.grid_rowconfigure(0, weight = 1)
bottomFrame.grid_columnconfigure(0, weight = 1)

#StatusBar Frame:
height_StatusBarFrame = 15
StatusBarFrame = Frame(root)
StatusBarFrame.config(height = height_StatusBarFrame)
StatusBarFrame.pack(side = "bottom", fill = "both", expand = False)
StatusBarFrame.grid_rowconfigure(0, weight = 1)
StatusBarFrame.grid_columnconfigure(0, weight = 1)
###########################################################################################
###########################################################################################


#Labels and Buttons:
###########################################################################################
###########################################################################################

# Title: Labels on topframes:
title_text = "FELion Spectrum Analyser"
title = Label(topFrame)
title.config(text = title_text, relief = SOLID, bd = 1, bg = "white",\
  font = "Times 15 bold", pady = 5)
title.pack(side = "top", fill = "both", expand = True)

sub_title_text = "Analysing FELIX data for FELion Instrument"
sub_title = Label(topFrame)
sub_title.config(text = sub_title_text, relief = FLAT, bg = "white",\
  font = "Times 12 italic", pady = 5, anchor = "e")
sub_title.pack(fill = "both", expand = True)


#Buttons:








#Status Bar: Labels on status bar frames:
statusBar_left_text = "Version 1.0"
statusBar_left = Label(StatusBarFrame)
statusBar_left.config(text = statusBar_left_text, \
  relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "w")
statusBar_left.pack(side = "top", fill = "both", expand = True)

statusBar_right_text = "Developed by Sandra's group (Aravindh) at FELIX"
statusBar_right = Label(StatusBarFrame)
statusBar_right.config(text = statusBar_right_text, \
  relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "e")
statusBar_right.pack(side = "top", fill = "both", expand = True)


root.mainloop()

###########################################################################################
###########################################################################################
