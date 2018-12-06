#!/usr/bin/python3

## A simple GUI program for FELion Instrument:
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#Importing FELion Modules:
from FELion_normline import normline_correction
from FELion_avgSpec import avgSpec_plot

def gui_normline():
    # User defined definitions:
    ###########################################################################################
    ###########################################################################################
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root = Tk()

    #Defining the main window's dimensions:
    width_window = 600
    height_window = 400
    root.geometry("{}x{}".format(width_window, height_window))
    root.title("FELion Spectrum Analyser")

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
    title_text = "Normline and Average"
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

    #Quit Button
    quitButton = ttk.Button(bottomFrame, text = "quit")
    quitButton.config(command = lambda: on_closing())
    ###########################################################################################
    ###########################################################################################

    ###########################################################################################
    #Normline
    normline_button = ttk.Button(bottomFrame, text="Normline")
    normline_button.config(command = lambda: normline_correction(content.get()))

    #Avg_Spectrum
    avg_button = ttk.Button(bottomFrame, text="Avg_spectrum")
    avg_button.config(command = lambda: avgSpec_plot())


    #Placing the labels and buttons in bottom frame using place(), relx/y is relative to parent frame pixels
    user_input_label.place(relx = 0.1,  rely = 0.1, width = 100, height = 40)
    user_input.place(relx = 0.3,  rely = 0.1, width = 100, height = 40)
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

    statusBar_right_text = "Developed at FELIX"
    statusBar_right = Label(StatusBarFrame)
    statusBar_right.config(text = statusBar_right_text, \
    relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "e")
    statusBar_right.pack(side = "top", fill = "both", expand = True)
    ###########################################################################################
    ###########################################################################################

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    return

if __name__ == "__main__":
    gui_normline()