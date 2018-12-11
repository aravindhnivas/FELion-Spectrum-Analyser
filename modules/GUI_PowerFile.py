#!/usr/bin/python3

from tkinter import *
from tkinter import ttk, messagebox

import os
import shutil
import time

def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
def locationnotfound(location):
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", "Location NOT FOUND".format(location))
        root.destroy()

def outFile(fname, location):


        try:
                os.chdir(location)
                my_path = os.getcwd()
                file = T.get("1.0", "end-1c")


                def saveinfo():
                        os.chdir(location)
                        if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                                save = Tk()
                                save.withdraw()
                                messagebox.showinfo("Information", \
                                        "File {}.pow saved in /Pow directory".format(fname))
                                save.destroy()

                def write():
                        f = open(my_path+"/Pow/{}.pow".format(fname), "w")
                        f.write(file)
                        f.close()
                        saveinfo()

                
                if not os.path.isdir("Pow"):
                        os.mkdir("Pow")

                if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                        if messagebox.askokcancel("Overwrite", \
                                "Do yo want to overwrite the existing {}.pow file?".format(fname)):
                                write()
                                
                else:
                        write()

        except:
                locationnotfound(location)

root = Tk()
width_window = 900
height_window = 500

root.geometry("{}x{}".format(width_window, height_window))

root.title("FELion Spectrum Analyser - Pow file generator:")

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
title_text = "Powerfile Generator:"
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

# Labels and buttons:

# Location:
location_label = Label(bottomFrame, text = "Location:", font=("Times", 10, "bold"))

location = StringVar()
location.set("Enter file lcoation here")
location_entry = Entry(bottomFrame, bg = "white", bd = 5,\
                        textvariable=location, justify = LEFT,\
                        font=("Times", 12, "italic"))


location_label.place(relx = 0.1,  rely = 0.1, width = 100, height = 40)
location_entry.place(relx = 0.3,  rely = 0.1, relwidth = 0.5, height = 40)

#Label for Entry Box;
user_input_label = Label(bottomFrame, text = " Filename:", font=("Times", 10, "bold"))

#Entry Box;
init_msg = "Enter here" #initialising message
content = StringVar()   #defining Stringvar()
user_input = Entry(bottomFrame, bg = "white", bd = 5, textvariable=content, justify = LEFT)
user_input.config(font=("Times", 12, "italic"))
user_input.focus_set()
content.set(init_msg)
###########################################################################################
###########################################################################################


#Baseline
save_button = ttk.Button(bottomFrame, text="Save")
save_button.config(command = lambda: outFile(content.get(), location.get()))

#Placing the labels and buttons in bottom frame using place(), relx/y is relative to parent frame pixels
user_input_label.place(relx = 0.1,  rely = 0.3, width = 100, height = 40)
user_input.place(relx = 0.3,  rely = 0.3, width = 100, height = 40)
save_button.place(relx = 0.5,  rely = 0.3, width = 100, height = 40)

T = Text(bottomFrame)
S = Scrollbar(bottomFrame)
T.config(yscrollcommand=S.set)
T.place(relx = 0.1,  rely = 0.5, relwidth = 0.7, relheight = 0.4)
S.config(command=T.yview)
S.place(relx = 0.8,  rely = 0.5, width = 15, relheight = 0.4)


quote = """\
#POWER file 
# 10 Hz FELIX
#
#SHOTS=26 
#INTERP=linear
#    IN_no_UM (if one deletes the "no" the firs number will be in \mu m
# wavelength/cm-1      energy/pulse/mJ"""

T.insert(END, quote)

###########################################################################################
###########################################################################################

#Status Bar: Labels on status bar frames:
statusBar_left_text = "Version 1.0"
statusBar_left = Label(StatusBarFrame)
statusBar_left.config(text = statusBar_left_text, \
relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "w")
statusBar_left.pack(side = "top", fill = "both", expand = True)

statusBar_right_text = "Developed at FELIX"
statusBar_right = Label(StatusBarFrame)
statusBar_right.config(text = statusBar_right_text, \
relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "e")
statusBar_right.pack(side = "top", fill = "both", expand = True)
###########################################################################################
###########################################################################################


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()