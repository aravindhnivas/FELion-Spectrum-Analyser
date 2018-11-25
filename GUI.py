#!/usr/bin/python3
#Importing all the required definitions from various functions
from tkinter import *
from tkinter import messagebox
from FELion_baseline import *
from FELion_normline import *
from FELion_avgSpec import *
###################################################################################################

#Custom definition:
#Definitions:
def input_file(*args):
    content.set(user_input.get())
    file_name = user_input.get()
    print(file_name)
    return file_name


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

#Defining root frame window
root = Tk()
root.title("FELion SPectrum Analyser")
# You can't drag the windows corner's to maximize or minimize the window
width_window = 775
height_window = 318
root.resizable(width=FALSE, height=FALSE)
#To make the window appear in the center:
your_computer_screen_width = root.winfo_screenwidth()
your_computer_screen_height = root.winfo_screenheight()
x_coordinate = (your_computer_screen_width/2) - (width_window/2) 
y_coordinate = (your_computer_screen_height/2) - (height_window/2)
root.geometry("%dx%d+%d+%d" %(width_window, height_window, x_coordinate, y_coordinate))

# Defining frames
topFrame = Frame(root, bg = "white", width=300, height=200)
middleFrame = Frame(root, bg = "green", width=300, height=200)
bottomFrame = Frame(root, bg = "green", width=300, height=200)

#Frame grids:
#Defining variables for geometry of frames padding:
xpad, ypad, ixpad, iypad = (0, 0, 0, 0)
topFrame.grid(row = 0, column = 0, padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)
middleFrame.grid(row = 1, column = 0, padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)
bottomFrame.grid(row = 2, column = 0, padx=xpad, pady=ypad, ipadx=ixpad, ipady=iypad)

#grid configure:
# "nsew" indicates - Noth, south, east and west. Making the row fill all the spot available.
topFrame.grid_configure(sticky = "nsew")
middleFrame.grid_configure(sticky = "nsew")
bottomFrame.grid_configure(sticky = "nsew")

#TOP Frames:
#TITLE:
title_text = "FELion Spectrum Analyser"
title_var = StringVar()
title_var.set(title_text)
title = Label(topFrame, relief = RAISED, bd = 2)
title.config(textvariable = title_var, bg = "white", \
    width=45, height=1, \
    font="Times 22 bold", \
    justify = CENTER, anchor = CENTER)

version_info_text = "For Analysing FELIX data for FELion Instrument"
version_info =  Label(topFrame)
version_info.config(text = version_info_text, bg = "white", width=45, height=1, \
    font="Times 12 italic")

#Title grids:
title.grid(row = 0, column = 0, padx=1, pady=1, ipady=5)
version_info.grid(row = 1, column = 0, sticky = E, padx=1, pady=1, ipady=1)

#MIDDLE FRAME:
#Label Entry Box;
user_input_label = Label(middleFrame)
user_input_label.config(text = " Enter filename\n(w/o .felix): ", \
                            width=15, height=2,\
                            font=("Times", 12, "bold"),
                            justify = CENTER,
                            anchor = CENTER)

#Text Entry Box;
init_msg = "Enter here" #initialising message
content = StringVar()   #defining Stringvar()
user_input = Entry(middleFrame, bg = "white", bd = 5, \
    textvariable=content, justify = LEFT)
user_input.config(font=("Times", 12, "italic"))
user_input.focus_set()
content.set(init_msg)
file_name = user_input.get() #storing user input value in filename

#Button Entry Box;
#Button for submitting:
Submit = Button(middleFrame)
Submit.config(text="Submit", relief=RAISED, width=20, height=1, command = input_file,\
    font=("Times", 12, "bold"))

#grid points for middleframe(location) label and entry column
user_input_label.grid(row = 0, column = 0, padx=2, pady=20, ipady=5)
user_input.grid(row = 0, column = 1,padx=2, pady=20, ipady=5)
Submit.grid(row = 0, column = 2, padx=2, pady=20, ipady=5)

#BOTTOM FRAME:
#Baseline
baseline_button = Button(bottomFrame, text="Baseline")
baseline_button.config(relief=RAISED, width=20, height=1, \
    command = lambda: baseline_correction(user_input.get()),\
    font=("Times", 12, "bold"))

#Normline
normline_button = Button(bottomFrame, text="Normline")
normline_button.config(relief=RAISED, width=20, height=1,
    command = lambda: normline(user_input.get()),\
    font=("Times", 12, "bold"))

#Avg_Spectrum
avg_button = Button(bottomFrame, text="Avg_spectrum")
avg_button.config(relief=RAISED, width=20, height=1,\
    command = lambda: avgSpec(user_input.get()),\
    font=("Times", 12, "bold"))

#Quit Button
quitButton = Button(bottomFrame)
quitButton.config(text="Quit", fg = "red", command=on_closing,\
    font=("Times", 12, "bold"), width=20, height=1)

#Save progm button
saveButton = Button(bottomFrame)
saveButton.config(text="Click to save baseline", fg = "green", command=root.quit,\
    font=("Times", 12, "bold"), width=20, height=1)

#Status bar:
statusBar_full = Label(bottomFrame, bg = "grey", relief = SUNKEN, bd = 2)
statusBar_text1 = "Version 1.0 (alpha)"
statusLabel_1 = Label(bottomFrame)
statusLabel_1.config(text = statusBar_text1, bg = "grey",\
    justify = LEFT, anchor = SW,\
    width = 20, height = 1)

statusBar_text2 = "Developed by Sandra's group (Aravindh) at FELIX"
statusLabel_2 = Label(bottomFrame)
statusLabel_2.config(text = statusBar_text2, \
    relief = SUNKEN, bg = "grey", \
    bd = 2, justify = LEFT, anchor = SE,\
    width = 25, height = 1)

#bottom frame grid location:
baseline_button.grid(row = 0, column = 0, padx=2, pady=2, ipady=5)
normline_button.grid(row = 0, column = 1, padx=2, pady=2, ipady=5)
avg_button.grid(row = 0, column = 2, padx=2, pady=2, ipady=5)
saveButton.grid(row = 1, column = 0, padx=2, pady=2, ipady=5)
quitButton.grid(row = 1, column = 4, padx=5, pady=20, ipady=2)
statusBar_full.grid(row = 2, columnspan = 5, sticky = "nsew")
statusLabel_1.grid(row = 2, column = 0, padx=5, pady=1, ipady=1)
statusLabel_2.grid(row = 2, column = 4, padx=5, pady=1, ipady=1)

#root.protocol("WM_DELETE_WINDOW", on_closing)
#Root mainloop
root.mainloop()

print("\n####################################     PROGRAM CLOSED     ####################################")
#EXIT
####################