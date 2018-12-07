#!/usr/bin/python3

## A simple GUI program for FELion Instrument:
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#Importing FELion Modules:
from FELion_normline import normline_correction
from FELion_avgSpec import avgSpec_plot


def avg_buttons():
    pass

def gui_normline():
    # User defined definitions:
    ###########################################################################################
    ###########################################################################################
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root = Tk()

    #Defining the main window's dimensions:
    width_window = 700
    height_window = 700
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

    

    # Avg_Spectrum Labels:
    avg_title = Label(bottomFrame, text = "Title:", font=("Times", 10, "bold"))
    avg_ts = Label(bottomFrame, text = "Title\nsize:", font=("Times", 10, "bold"))
    avg_lgs = Label(bottomFrame, text = "Legend\nSize:", font=("Times", 10, "bold"))
    avg_minor = Label(bottomFrame, text = "Minor\naxis:", font=("Times", 10, "bold"))
    avg_major = Label(bottomFrame, text = "Major\naxis:", font=("Times", 10, "bold"))
    avg_majorTick = Label(bottomFrame, text = "Major\nTickSz:", font=("Times", 10, "bold"))
    avg_xmin = Label(bottomFrame, text = "X-min:", font=("Times", 10, "bold"))
    avg_xmax = Label(bottomFrame, text = "X-max:", font=("Times", 10, "bold"))

    # avg_label's Entry widget:
    i_avg_title = StringVar()
    i_avg_ts = IntVar() 
    i_avg_lgs = IntVar() 
    i_avg_minor = IntVar() 
    i_avg_major = IntVar() 
    i_avg_majorTick = IntVar() 
    i_avg_xmin = IntVar() 
    i_avg_xmax = IntVar()
        
    i_avg_title.set("Title")
    i_avg_ts.set(10)
    i_avg_lgs.set(5)
    i_avg_minor.set(5)
    i_avg_major.set(50)
    i_avg_majorTick.set(8)
    i_avg_xmin.set(1000)
    i_avg_xmax.set(2000)

    avg_title_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_title, justify = LEFT, font=("Times", 10, "bold"))
    avg_ts_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_ts, justify = LEFT, font=("Times", 10, "bold"))
    avg_lgs_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_lgs, justify = LEFT, font=("Times", 10, "bold"))
    avg_minor_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_minor, justify = LEFT, font=("Times", 10, "bold"))
    avg_major_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_major, justify = LEFT, font=("Times", 10, "bold"))
    avg_majorTick_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_majorTick, justify = LEFT, font=("Times", 10, "bold"))
    avg_xmin_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_xmin, justify = LEFT, font=("Times", 10, "bold"))
    avg_xmax_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_xmax, justify = LEFT, font=("Times", 10, "bold"))
    
    # Placing the avg_labels and Entry widgets:
    avg_title.place(relx = 0.5,  rely = 0.1, width = 100, height = 40)
    avg_ts.place(relx = 0.5,  rely = 0.2, width = 100, height = 40)
    avg_lgs.place(relx = 0.5,  rely = 0.3, width = 100, height = 40)
    avg_minor.place(relx = 0.5,  rely = 0.4, width = 100, height = 40)
    avg_major.place(relx = 0.5,  rely = 0.5, width = 100, height = 40)
    avg_majorTick.place(relx = 0.5,  rely = 0.6, width = 100, height = 40)
    avg_xmin.place(relx = 0.5,  rely = 0.7, width = 100, height = 40)
    avg_xmax.place(relx = 0.5,  rely = 0.8, width = 100, height = 40)

    avg_title_Entry.place(relx = 0.7,  rely = 0.1, width = 100, height = 40)
    avg_ts_Entry.place(relx = 0.7,  rely = 0.2, width = 100, height = 40)
    avg_lgs_Entry.place(relx = 0.7,  rely = 0.3, width = 100, height = 40)
    avg_minor_Entry.place(relx = 0.7,  rely = 0.4, width = 100, height = 40)
    avg_major_Entry.place(relx = 0.7,  rely = 0.5, width = 100, height = 40)
    avg_majorTick_Entry.place(relx = 0.7,  rely = 0.6, width = 100, height = 40)
    avg_xmin_Entry.place(relx = 0.7,  rely = 0.7, width = 100, height = 40)
    avg_xmax_Entry.place(relx = 0.7,  rely = 0.8, width = 100, height = 40)

    #Avg_Spectrum
    avg_button = ttk.Button(bottomFrame, text="Avg_spectrum")
    avg_button.config(command = lambda: avgSpec_plot(i_avg_title.get(), \
                                                            i_avg_ts.get(), \
                                                            i_avg_lgs.get(), \
                                                            i_avg_minor.get(), \
                                                            i_avg_major.get(), \
                                                            i_avg_majorTick.get(), \
                                                            i_avg_xmin.get(), \
                                                            i_avg_xmax.get())
                                                            )

    #Placing the labels and buttons in bottom frame using place(), relx/y is relative to parent frame pixels
    user_input_label.place(relx = 0.1,  rely = 0.1, width = 100, height = 40)
    user_input.place(relx = 0.3,  rely = 0.1, width = 100, height = 40)
    normline_button.place(relx = 0.1,  rely = 0.3, width = 100, height = 40)
    avg_button.place(relx = 0.3,  rely = 0.3, width = 100, height = 40)
    quitButton.place(relx = 0.2,  rely = 0.9, width = 100, height = 40)

    

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