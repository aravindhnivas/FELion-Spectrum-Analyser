#!/usr/bin/python3


from tkinter import *
from tkinter import ttk, messagebox

def centerIt(root, width_window, height_window):
    #Making window appear at the center of your computer screen:
    your_computer_screen_width = root.winfo_screenwidth()
    your_computer_screen_height = root.winfo_screenheight()
    x_coordinate = (your_computer_screen_width/2) - (width_window/2)
    y_coordinate = (your_computer_screen_height/2) - (height_window/2)
    return root.geometry("%dx%d+%d+%d" %(width_window, height_window, x_coordinate, y_coordinate))

def framesandlabels(root,\
                    bg_color,\
                    title_text, \
                    sub_title_text, \
                    statusBar_left_text, \
                    statusBar_right_text):
    #Frames:
    ###########################################################################################
    ###########################################################################################
    #bg_color = "sea green"
    height_topFrame = 100
    height_StatusBarFrame = 15

    #top frames:
    topFrame = Frame(root, height = height_topFrame)
    topFrame.pack(side = "top", fill = "both", expand = False)

    #bottom frames
    bottomFrame = Frame(root, bg = bg_color)
    bottomFrame.pack(side = "top", fill = "both", expand = True)

    #StatusBar Frame:
    StatusBarFrame = Frame(root, height = height_StatusBarFrame)
    StatusBarFrame.pack(side = "bottom", fill = "both", expand = False)

    # Title: Labels on topframes:
    #title_text = "Baseline Correction"
    title = Label(topFrame)
    title.config(text = title_text, relief = SOLID, bd = 1, bg = bg_color,\
    font = "Times 15 bold", pady = 5)
    title.pack(side = "top", fill = "both", expand = True)

    #sub_title_text = "Analysing FELIX data for FELion Instrument"
    sub_title = Label(topFrame)
    sub_title.config(text = sub_title_text, relief = FLAT, bg = bg_color,\
    font = "Times 12 italic", pady = 5, anchor = "e")
    sub_title.pack(fill = "both", expand = True)

    #Status Bar: Labels on status bar frames:
    #statusBar_left_text = "Version 1.0"
    statusBar_left = Label(StatusBarFrame)
    statusBar_left.config(text = statusBar_left_text, \
    relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "w")
    statusBar_left.pack(side = "top", fill = "both", expand = True)

    #statusBar_right_text = "Developed at FELIX"
    statusBar_right = Label(StatusBarFrame)
    statusBar_right.config(text = statusBar_right_text, \
    relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "e")
    statusBar_right.pack(side = "top", fill = "both", expand = True)
    ###########################################################################################
    ###########################################################################################
    return bottomFrame


def locationframe(bottomFrame, xl = 0.1, yl = 0.1, lw = 100, lh = 50,\
                    xe = 0.3, ye = 0.1, erw = 0.5, eh =  50):

    location_label = Label(bottomFrame, text = "Location:", font=("Times", 10, "bold"))

    location = StringVar()
    location.set("Enter file lcoation here")
    location_entry = Entry(bottomFrame, bg = "white", bd = 5,\
                            textvariable=location, justify = LEFT,\
                            font=("Times", 12, "italic"))


    location_label.place(relx = xl,  rely = yl, width = lw, height = lh)
    location_entry.place(relx = xe,  rely = ye, relwidth = erw, height = eh)