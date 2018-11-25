## A simple GUI program for FELion Instrument:

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#Importing definitions from FELion python modules:
from FELion_baseline import baseline_correction
from FELion_normline import normline
from FELion_avgSpec import avgSpec

# User defined definitions:
def on_closing():
  if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.destroy()



#Main configuration:
###########################################################################################
###########################################################################################
root = Tk()

#Defining the main window's dimensions:
width_window = 600
height_window = 400

#Making window appear at the center of your computer screen:
your_computer_screen_width = root.winfo_screenwidth()
your_computer_screen_height = root.winfo_screenheight()
x_coordinate = (your_computer_screen_width/2) - (width_window/2)
y_coordinate = (your_computer_screen_height/2) - (height_window/2)
root.geometry("%dx%d+%d+%d" %(width_window, height_window, x_coordinate, y_coordinate))

#Defining the window titile
root.title("FELion Spectrum Analyser")

###########################################################################################
###########################################################################################

#Frames:
###########################################################################################
###########################################################################################

height_topFrame = 100
height_StatusBarFrame = 15

#top frames:
topFrame = Frame(root, height = height_topFrame)
topFrame.pack(side = "top", fill = "both", expand = False)

#bottom frames
bottomFrame = Frame(root, bg = "sea green")
bottomFrame.pack(side = "top", fill = "both", expand = True)

#StatusBar Frame:
StatusBarFrame = Frame(root, height = height_StatusBarFrame)
StatusBarFrame.pack(side = "bottom", fill = "both", expand = False)
###########################################################################################
###########################################################################################


#Labels and Buttons:
###########################################################################################
###########################################################################################

# Title: Labels on topframes:
title_text = "FELion Spectrum Analyser"
title = Label(topFrame)
title.config(text = title_text, relief = SOLID, bd = 1, bg = "sea green",\
  font = "Times 15 bold", pady = 5)
title.pack(side = "top", fill = "both", expand = True)

sub_title_text = "Analysing FELIX data for FELion Instrument"
sub_title = Label(topFrame)
sub_title.config(text = sub_title_text, relief = FLAT, bg = "sea green",\
  font = "Times 12 italic", pady = 5, anchor = "e")
sub_title.pack(fill = "both", expand = True)
###########################################################################################
###########################################################################################

#Buttons:
#Label for Entry Box;
user_input_label = Label(bottomFrame)
user_input_label.config(text = " Enter filename\n(w/o .felix): ", \
  font=("Times", 10, "bold"))

#Entry Box;
init_msg = "Enter here" #initialising message
content = StringVar()   #defining Stringvar()
user_input = Entry(bottomFrame, bg = "white", bd = 5, \
    textvariable=content, justify = LEFT)
user_input.config(font=("Times", 12, "italic"))
user_input.focus_set()
content.set(init_msg)
###########################################################################################
###########################################################################################

#Baseline
baseline_button = ttk.Button(bottomFrame, text="Baseline")
baseline_button.config(command = lambda: baseline_correction(user_input.get()))

#Save progm button
saveButton = ttk.Button(bottomFrame, text = "Save Baseline")
saveButton.config(command = root.quit)

#Normline
normline_button = ttk.Button(bottomFrame, text="Normline")
normline_button.config(command = lambda: normline(user_input.get()))

#Avg_Spectrum
avg_button = ttk.Button(bottomFrame, text="Avg_spectrum")
avg_button.config(command = lambda: avgSpec(user_input.get()))

###########################################################################################
###########################################################################################

#Quit Button
quitButton = ttk.Button(bottomFrame, text = "quit")
quitButton.config(command = root.destroy)
###########################################################################################
###########################################################################################

#Placing the labels and buttons in bottom frame using place(), relx/y is relative to parent frame pixels
user_input_label.place(relx = 0.1,  rely = 0.1, width = 100, height = 40)
user_input.place(relx = 0.3,  rely = 0.1, width = 100, height = 40)
baseline_button.place(relx = 0.1,  rely = 0.3, width = 100, height = 40)
saveButton.place(relx = 0.1,  rely = 0.5, width = 100, height = 40)
normline_button.place(relx = 0.3,  rely = 0.3, width = 100, height = 40)
avg_button.place(relx = 0.5,  rely = 0.3, width = 100, height = 40)
quitButton.place(relx = 0.3,  rely = 0.7, width = 100, height = 40)

###########################################################################################
###########################################################################################

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
###########################################################################################
###########################################################################################

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
###########################################################################################
###########################################################################################