#!/usr/bin/python3

## A simple GUI program for FELion Instrument:
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#Importing FELion Modules:
from FELion_normline import normline_correction
from FELion_avgSpec import avgSpec_plot
from FELion_sa import FELion_Sa
from FELion_power import FELion_Power
from FELion_massSpec import massSpec

def gui_normline():
    # User defined definitions:
    ###########################################################################################
    ###########################################################################################
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root = Tk()
    root.title("FELion Spectrum Analyser")


    #Defining the main window's dimensions:
    width_window = 1200
    height_window = 700

    root.geometry("{}x{}".format(width_window, height_window))

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
    title_text = "Normline, Average and Mass Spectrum"
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

    # Labels and Buttons:

    # Location:
    location_label = Label(bottomFrame, text = "Location:", font=("Times", 10, "bold"))

    location = StringVar()
    location.set("Enter file lcoation here")
    location_entry = Entry(bottomFrame, bg = "white", bd = 5,\
                                textvariable=location, justify = LEFT,\
                                font=("Times", 12, "italic"))

    location_label.place(relx = 0.1,  rely = 0.8, width = 100, height = 40)
    location_entry.place(relx = 0.2,  rely = 0.8, relwidth = 0.4, height = 40)

    #Label for Entry Box;
    filename_label = Label(bottomFrame, text = " Filename:", font=("Times", 10, "bold"))

    init_msg = "Enter here" #initialising message
    fname = StringVar()   #defining Stringvar()
    fname.set(init_msg)
    filename_input = Entry(bottomFrame, bg = "white", bd = 5, textvariable=fname, justify = LEFT)
    filename_input.config(font=("Times", 12, "italic"))
    filename_input.focus_set()

    #Placing the labels and buttons in bottom frame using place(), relx/y is relative to parent frame pixels
    filename_label.place(relx = 0.1,  rely = 0.7, width = 100, height = 40)
    filename_input.place(relx = 0.2,  rely = 0.7, width = 100, height = 40)

    ###########################################################################################
    ###########################################################################################

    #Quit Button
    quitButton = ttk.Button(bottomFrame, text = "quit")
    quitButton.config(command = lambda: on_closing())
    quitButton.place(relx = 0.9,  rely = 0.9, width = 100, height = 40)

    ###########################################################################################
    ###########################################################################################

    ###########################################################################################
    #Normline
    normline_button = ttk.Button(bottomFrame, text="Normline")
    normline_button.config(
        command = lambda: normline_correction(
                                    fname.get(), location.get(),\
                                    mname.get(), temp.get(), bwidth.get(), ie.get()
                                    )
                                    )
    normline_button.place(relx = 0.4,  rely = 0.9, width = 100, height = 40)

    # avg_labels's label:
    avg_label = Label(bottomFrame, text = "For Average Spectrum", font=("Times", 12, "italic"))
    avg_label.place(relx = 0.4,  rely = 0, relwidth = 0.2, height = 40)

    # Avg_Spectrum Labels:
    avg_title = Label(bottomFrame, text = "Title:", font=("Times", 10, "bold"))
    avg_ts_ls = Label(bottomFrame, text = "Size\n(Title, Legends):", font=("Times", 10, "bold"))
    avg_xaxis_count = Label(bottomFrame, text = "X-axis\nticks div.:", font=("Times", 10, "bold"))
    avg_majorTick = Label(bottomFrame, text = "Major\nTickSz:", font=("Times", 10, "bold"))
    avg_xaxis = Label(bottomFrame, text = "Range(cm-1):", font=("Times", 10, "bold"))

    # Placing the avg_labels
    avg_title.place(relx = 0.4,  rely = 0.1, width = 100, height = 40)
    avg_ts_ls.place(relx = 0.4,  rely = 0.2, width = 100, height = 40)
    avg_xaxis_count.place(relx = 0.4,  rely = 0.3, width = 100, height = 40)
    avg_majorTick.place(relx = 0.4,  rely = 0.4, width = 100, height = 40)
    avg_xaxis.place(relx = 0.4,  rely = 0.5, width = 100, height = 40)

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

    avg_title_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_title, justify = LEFT, font=("Times", 12, "italic"))
    avg_ts_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_ts, justify = LEFT, font=("Times", 10, "bold"))
    avg_lgs_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_lgs, justify = LEFT, font=("Times", 10, "bold"))
    avg_minor_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_minor, justify = LEFT, font=("Times", 10, "bold"))
    avg_major_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_major, justify = LEFT, font=("Times", 10, "bold"))
    avg_majorTick_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_majorTick, justify = LEFT, font=("Times", 10, "bold"))
    avg_xmin_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_xmin, justify = LEFT, font=("Times", 10, "bold"))
    avg_xmax_Entry = Entry(bottomFrame, bg = "white", bd = 5, textvariable=i_avg_xmax, justify = LEFT, font=("Times", 10, "bold"))

    # Placing the avg_entry widgets:
    avg_title_Entry.place(relx = 0.5,  rely = 0.1, width = 100, height = 40)
    avg_ts_Entry.place(relx = 0.5,  rely = 0.2, width = 50, height = 40)
    avg_lgs_Entry.place(relx = 0.55,  rely = 0.2, width = 50, height = 40)
    avg_minor_Entry.place(relx = 0.5,  rely = 0.3, width = 50, height = 40)
    avg_major_Entry.place(relx = 0.55,  rely = 0.3, width = 50, height = 40)
    avg_majorTick_Entry.place(relx = 0.5,  rely = 0.4, width = 100, height = 40)
    avg_xmin_Entry.place(relx = 0.5,  rely = 0.5, width = 50, height = 40)
    avg_xmax_Entry.place(relx = 0.55,  rely = 0.5, width = 50, height = 40)

    # avg spectrum output filename:
    avg_outputFilename = Label(bottomFrame, \
        text = "Output filename(Average)\n(also for Mass_combine)", font=("Times", 10, "bold"))

    output_filename = StringVar()
    output_filename.set("Average")
    avg_outputFilename_entry = Entry(bottomFrame, bg = "white", bd = 5, \
        textvariable=output_filename, justify = LEFT, font=("Times", 12, "italic"))

    # Placing avg_out filename labels and entry
    avg_outputFilename.place(relx = 0.4,  rely = 0.6, width = 150, height = 50)
    avg_outputFilename_entry.place(relx = 0.55,  rely = 0.6, width = 100, height = 50)

    #Avg_Spectrum Button
    specificFiles_status = False
    allFiles_status = True
    avg_button = ttk.Button(bottomFrame, text="Avg_spectrum")
    avg_button.config(command = lambda: avgSpec_plot(
                                                    i_avg_title.get(), \
                                                    i_avg_ts.get(), \
                                                    i_avg_lgs.get(), \
                                                    i_avg_minor.get(), \
                                                    i_avg_major.get(), \
                                                    i_avg_majorTick.get(), \
                                                    i_avg_xmin.get(), \
                                                    i_avg_xmax.get(),\
                                                    output_filename.get(),\
                                                    location.get(),\
                                                    mname.get(), temp.get(), bwidth.get(), ie.get(),\
                                                    specificFiles=specificFiles_status,\
                                                    allFiles=allFiles_status),\
                                                    )

    avg_button.place(relx = 0.5,  rely = 0.9, width = 100, height = 40)

    # Spectrum Analyzer and power Analyzer Buttons:
    sa_button = ttk.Button(bottomFrame, text="SA", \
        command = lambda: FELion_Sa(fname.get(), location.get()))
    power_button = ttk.Button(bottomFrame, text = "Power", \
        command = lambda: FELion_Power(fname.get(), location.get()))
    # Placing SA and power buttons:
    sa_button.place(relx = 0.2,  rely = 0.9, width = 100, height = 40)
    power_button.place(relx = 0.3,  rely = 0.9, width = 100, height = 40)

    # Initial Setting label:
    initial_set_label = Label(bottomFrame, text = "Spectra Parameters", font=("Times", 12, "italic"))
    initial_set_label.place(relx = 0.1,  rely = 0, relwidth = 0.2, height = 40)
    # the compund details:
    molecule_name_label = Label(bottomFrame, text = "Molecule", font=("Times", 10, "bold"))
    temp_label = Label(bottomFrame, text = "TEMP(K)", font=("Times", 10, "bold"))
    bwidth_label = Label(bottomFrame, text = "B0 Width(ms)", font=("Times", 10, "bold"))
    ion_enrg_label = Label(bottomFrame, text = "IE(eV)", font=("Times", 10, "bold"))

    molecule_name_label.place(relx = 0.1,  rely = 0.1, width = 100, height = 40)
    temp_label.place(relx = 0.1,  rely = 0.2, width = 100, height = 40)
    bwidth_label.place(relx = 0.1,  rely = 0.3, width = 100, height = 40)
    ion_enrg_label.place(relx = 0.1,  rely = 0.4, width = 100, height = 40)

    mname = StringVar()
    temp = StringVar()
    bwidth = StringVar()
    ie = StringVar()

    mname.set("Molecule")
    temp.set("-")
    bwidth.set("-")
    ie.set("-")

    molecule_name = Entry(bottomFrame, bg = "white", bd = 5, textvariable=mname, justify = LEFT, font=("Times", 12, "italic"))
    temperature = Entry(bottomFrame, bg = "white", bd = 5, textvariable=temp, justify = LEFT, font=("Times", 12, "italic"))
    bo_Width = Entry(bottomFrame, bg = "white", bd = 5, textvariable=bwidth, justify = LEFT, font=("Times", 12, "italic"))
    ion_enrg = Entry(bottomFrame, bg = "white", bd = 5, textvariable=ie, justify = LEFT, font=("Times", 12, "italic"))

    molecule_name.place(relx = 0.2,  rely = 0.1, width = 100, height = 40)
    temperature.place(relx = 0.2,  rely = 0.2, width = 100, height = 40)
    bo_Width.place(relx = 0.2,  rely = 0.3, width = 100, height = 40)
    ion_enrg.place(relx = 0.2,  rely = 0.4, width = 100, height = 40)

    # Mass Spectrum:

    # Initial Setting label:
    mass_init_label = Label(bottomFrame, text = "For MassSpectrum", \
                                font=("Times", 12, "italic"))
    mass_init_label.place(relx = 0.7,  rely = 0, relwidth = 0.2, height = 40)

    massSpec_label = Label(bottomFrame, text = "Mass_file: ", font=("Times", 10, "bold"))

    mass = StringVar()
    mass.set("Enter here")
    massSpec_input = Entry(bottomFrame, bg = "white", bd = 5, \
        textvariable=mass, justify = LEFT, font=("Times", 12, "italic"))
        
    mass_button = ttk.Button(bottomFrame, text="MassSpec", \
                                command = lambda: massSpec(\
                                    mass.get(), mname.get(), temp.get(), bwidth.get(), ie.get(),\
                                    mass_xmin.get(), mass_xmax.get(),\
                                    location.get(),\
                                    m_figwidth.get(), m_figheight.get(),\
                                    combine_entry_values.get(),\
                                    output_filename.get(),\
                                    mass_method_value.get()
                                    )
                            )

    #Placing mass spec:
    massSpec_label.place(relx = 0.7,  rely = 0.1, width = 100, height = 40)
    massSpec_input.place(relx = 0.8,  rely = 0.1, width = 100, height = 40)
    mass_button.place(relx = 0.75,  rely = 0.7, width = 100, height = 40)

    # Mass Spec labels:
    mass_range_label = Label(bottomFrame, text = "Range(u):", font=("Times", 10, "bold"))

    mass_xmin = IntVar()
    mass_xmax = IntVar()
    mass_xmin.set(0)
    mass_xmax.set(80)
    mass_xmin_Entry = Entry(bottomFrame, bg = "white", bd = 5, \
        textvariable=mass_xmin, justify = LEFT, font=("Times", 10, "bold"))
    mass_xmax_Entry = Entry(bottomFrame, bg = "white", bd = 5, \
        textvariable=mass_xmax, justify = LEFT, font=("Times", 10, "bold"))

    mass_figsize = Label(bottomFrame, text = "FigSize:", font=("Times", 10, "bold"))

    m_figwidth = IntVar()
    m_figheight = IntVar()

    m_figwidth.set(7)
    m_figheight.set(5)
    mass_figWidth = Entry(bottomFrame, bg = "white", bd = 5, textvariable=m_figwidth, justify = LEFT, font=("Times", 10, "bold"))
    mass_figHeight = Entry(bottomFrame, bg = "white", bd = 5, textvariable=m_figheight, justify = LEFT, font=("Times", 10, "bold"))

    mass_range_label.place(relx = 0.7,  rely = 0.2, width = 100, height = 40)
    mass_xmin_Entry.place(relx = 0.8,  rely = 0.2, width = 50, height = 40)
    mass_xmax_Entry.place(relx = 0.85,  rely = 0.2, width = 50, height = 40)
    mass_figsize.place(relx = 0.7,  rely = 0.3, width = 100, height = 40)
    mass_figWidth.place(relx = 0.8,  rely = 0.3, width = 50, height = 40)
    mass_figHeight.place(relx = 0.85,  rely = 0.3, width = 50, height = 40)


        
    #Combine Mass spec:
    def combine_func(combine):
        display_label = Label(bottomFrame, font=("Times", 10, "italic"))

        if not combine:
            display_label.config(text = "Single mode active:")
            display_label.place(relx = 0.7,  rely = 0.5, relwidth = 0.2, height = 40)

        if combine:
            display_label.config(text = "Combine mode active:")
            display_label.place(relx = 0.7,  rely = 0.5, relwidth = 0.2, height = 40)
            


    mass_method_value = BooleanVar()
    single_mass = ttk.Radiobutton(bottomFrame, text = "Single: ", \
        variable = mass_method_value, value = False, \
        command = lambda: combine_func(mass_method_value.get()))
    combine_mass = ttk.Radiobutton(bottomFrame, text = "Combine: ", \
        variable = mass_method_value, value = True, \
        command = lambda: combine_func(mass_method_value.get()))

    single_mass.place(relx = 0.7,  rely = 0.4, width = 100, height = 40)
    combine_mass.place(relx = 0.8,  rely = 0.4, width = 100, height = 40)
        

    combine_entry_values = StringVar()
    combine_entry_values.set("Combine: Enter just files nos. (if same data)")

    combine_entry = Entry(bottomFrame, bg = "white", bd = 5,\
                            textvariable=combine_entry_values, justify = LEFT,\
                            font=("Times", 12, "italic"))
    combine_entry.place(relx = 0.7,  rely = 0.6, relwidth = 0.2, height = 50)

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