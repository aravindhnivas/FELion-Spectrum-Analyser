#!/usr/bin/python3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import datetime
import matplotlib.pyplot as plt
from timescan_plot import timescanplot

#FELion modules
from FELion_massSpec import massSpec
from FELion_avgSpec import avgSpec_plot
from FELion_normline import normline_correction
from FELion_power import FELion_Power
from FELion_sa import FELion_Sa
from FELion_definitions import *

from tkfilebrowser import askopenfilenames
from os.path import join

def outFile(fname, location, file):
        try:
                os.chdir(location)
                my_path = os.getcwd()
 
                def saveinfo():
                        os.chdir(location)
                        if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                                ShowInfo("SAVED", "File %s.pow saved in /Pow directory"%fname)
                                

                def write():
                        f = open(my_path+"/Pow/{}.pow".format(fname), "w")
                        f.write(file)
                        f.close()
                        saveinfo()

                
                if not os.path.isdir("Pow"): os.mkdir("Pow") 

                if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                        messagebox.showerror("OVERWRITE","File already exist")
                        if messagebox.askokcancel("OVERWRITE", \
                                "Do yo want to overwrite the existing {}.pow file?".format(fname)):
                                write()
                                
                else:
                        write()

        except Exception as e:
                ErrorInfo("ERROR", e)

LARGE_FONT= ("Verdana", 15)
diff = 0.15
x1 = 0.15
x2 = x1 + diff
x3 = x2 + diff
x4 = x3 + diff
x5 = x4 + diff + 0.07

y = 0.9
width, height = (100, 40)
smallwidth = 50

class FELion(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        Tk.iconbitmap(self,default='C:/FELion-GUI/software/FELion_Icon.ico')
        Tk.wm_title(self, "FELion-Spectrum Analyser v.2.0")
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

        for F in (StartPage, Normline, Mass, Powerfile, Plot):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")
        
        label = Label(self, text="Start Page", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        button1 = ttk.Button(self, text="Norm and Avg",
                            command=lambda: controller.show_frame(Normline))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Mass Spec",
                            command=lambda: controller.show_frame(Mass))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Powerfile",
                            command=lambda: controller.show_frame(Powerfile))
        button3.place(relx = x3, rely = y, width = width, height = height)

        button4 = ttk.Button(self, text="Plot",
                            command=lambda: controller.show_frame(Plot))
        button4.place(relx = x4, rely = y, width = width, height = height)

        button5 = ttk.Button(self, text="Update Program",
                            command=lambda: update())
        button5.place(relx = x5, rely = y, width = 110, height = height)

        welcome_msg = """
        The FELion Spectrum analyser for analysing FELIX data using Python;

        It consists: the following functions:
                1. Normline and Average Spectrum Plot
                2. Mass Spectrum Plot
                3. Powerfile Generator
                4. Plot (For general X,Y plots:)
                5. Update Program (For updating to the latest version from github)

        NOTE: Before using Normline and Average Spectrum plot functions: 
        Make sure you already did "Baseline Correction" using "FELion_Baseline" Program

        If error: Maybe, try to avoid using //server as the location

        The processed raw data output files can be found in "EXPORT" and "DATA" folder.
        The processed output files can be found in "OUT" and "MassSpec_DATA"

        Report bug/suggestion: aravindh@science.ru.nl
        """
        label = Label(self, text=welcome_msg, justify = "left",\
                font=("Verdana", 11, "italic"), bg="sea green")
        label.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.75)

class Normline(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")
        
        label = Label(self, text="Normline", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Mass Spec",
                            command=lambda: controller.show_frame(Mass))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Powerfile",
                            command=lambda: controller.show_frame(Powerfile))
        button3.place(relx = x3, rely = y, width = width, height = height)

        button4 = ttk.Button(self, text="Plot",
                            command=lambda: controller.show_frame(Plot))
        button4.place(relx = x4, rely = y, width = width, height = height)

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

        #Normline
        fname_label = Label(self, text = "Filename: ", font=("Times", 10, "bold"))

        # the compund details:
        molecule_name_label = Label(self, text = "Molecule", font=("Times", 10, "bold"))
        temp_label = Label(self, text = "TEMP(K)", font=("Times", 10, "bold"))
        bwidth_label = Label(self, text = "B0 Width(ms)", font=("Times", 10, "bold"))
        ion_enrg_label = Label(self, text = "IE(eV)", font=("Times", 10, "bold"))

        mname = StringVar()
        temp = StringVar()
        bwidth = StringVar()
        ie = StringVar()

        mname.set("Molecule")
        temp.set("-")
        bwidth.set("-")
        ie.set("-")

        molecule_name = Entry(self, bg = "white", bd = 5, textvariable=mname, justify = LEFT, font=("Times", 12, "italic"))
        temperature = Entry(self, bg = "white", bd = 5, textvariable=temp, justify = LEFT, font=("Times", 12, "italic"))
        bo_Width = Entry(self, bg = "white", bd = 5, textvariable=bwidth, justify = LEFT, font=("Times", 12, "italic"))
        ion_enrg = Entry(self, bg = "white", bd = 5, textvariable=ie, justify = LEFT, font=("Times", 12, "italic"))

        foravgshow = False
        normline_button = ttk.Button(self, text="Normline")
        normline_button.config(
                command = lambda: normline_correction(
                                        self.fname, self.location,\
                                        mname.get(), temp.get(), bwidth.get(), ie.get(),\
                                        normavg_saveCheck_value.get(),\
                                        foravgshow, normallCheck_value.get(), norm_show_value.get()
                                        )
                                        )
        

        # Save checkbutton for normall:
        normallCheck_value = BooleanVar()
        normallCheck_value.set(False)
        normallCheck = ttk.Checkbutton(self, text = "Plot all files at once", variable = normallCheck_value)
        

        # Show checkbutton for Normline:
        norm_show_value = BooleanVar()
        norm_show_value.set(True)
        norm_show = ttk.Checkbutton(self, text = "Show", variable = norm_show_value)
        

        # avg_labels's label:
        avg_label = Label(self, text = "For Average Spectrum", font=("Times", 12, "italic"))

        delta_label = Label(self, text = "DELTA", font = "Times 12 italic")

        delta = IntVar()
        delta.set(2)
        delta_value = Entry(self, bg = "white", bd = 5, textvariable=delta, justify = LEFT, font=("Times", 12, "italic"))
        
        

        # Avg_Spectrum Labels:
        avg_title = Label(self, text = "Title:", font=("Times", 10, "bold"))
        avg_ts_ls = Label(self, text = "Size\n(Title,Legend)", font=("Times", 10, "bold"))
        avg_xaxis_count = Label(self, text = "X-axis\nticks div:", font=("Times", 10, "bold"))
        avg_majorTick = Label(self, text = "Major TickSz,\nMarkerSz:", font=("Times", 10, "bold"))

        avg_xywf = Label(self, text = "X,Y,Wid,Ht", font=("Times", 10, "bold"))

        # avg_label's Entry widget:
        i_avg_title = StringVar()
        i_avg_ts = IntVar() 
        i_avg_lgs = IntVar() 
        i_avg_minor = IntVar() 
        i_avg_major = IntVar() 
        i_avg_majorTick = IntVar()

        i_avg_xlabelsz = IntVar()
        i_avg_ylabelsz= IntVar()
        i_avg_fwidth= IntVar()
        i_avg_fheight= IntVar()
        i_avg_markersz = IntVar()
        
                
        i_avg_title.set("Title")
        i_avg_ts.set(15)
        i_avg_lgs.set(10)
        i_avg_minor.set(20)
        i_avg_major.set(100)
        i_avg_majorTick.set(15)
        i_avg_markersz.set(2)

        i_avg_xlabelsz.set(15)
        i_avg_ylabelsz.set(15)
        i_avg_fwidth.set(10)
        i_avg_fheight.set(5)

        avg_title_Entry = Entry(self, bg = "white", bd = 5, textvariable=i_avg_title, justify = LEFT, font=("Times", 12, "italic"))
        avg_ts_Entry = Entry(self, bg = "white", bd = 5, textvariable=i_avg_ts, justify = LEFT, font=("Times", 10, "bold"))
        avg_lgs_Entry = Entry(self, bg = "white", bd = 5, textvariable=i_avg_lgs, justify = LEFT, font=("Times", 10, "bold"))
        avg_minor_Entry = Entry(self, bg = "white", bd = 5, textvariable=i_avg_minor, justify = LEFT, font=("Times", 10, "bold"))
        avg_major_Entry = Entry(self, bg = "white", bd = 5, textvariable=i_avg_major, justify = LEFT, font=("Times", 10, "bold"))
        avg_majorTick_Entry = Entry(self, bg = "white", bd = 5, textvariable=i_avg_majorTick, justify = LEFT, font=("Times", 10, "bold"))
        avg_markersize_Entry = Entry(self, bg = "white", bd = 5, textvariable=i_avg_markersz, justify = LEFT, font=("Times", 10, "bold"))


        avg_xlabelsz = Entry(self, bg = "white", bd = 5, textvariable=i_avg_xlabelsz, justify = LEFT, font=("Times", 12, "italic"))
        avg_ylabelsz = Entry(self, bg = "white", bd = 5, textvariable=i_avg_ylabelsz, justify = LEFT, font=("Times", 12, "italic"))
        avg_fwidth = Entry(self, bg = "white", bd = 5, textvariable=i_avg_fwidth, justify = LEFT, font=("Times", 12, "italic"))
        avg_fheight = Entry(self, bg = "white", bd = 5, textvariable=i_avg_fheight, justify = LEFT, font=("Times", 12, "italic"))

        # avg spectrum output filename:
        avg_outputFilename = Label(self, \
                text = "Out. filename\n(Average)", font=("Times", 10, "bold"))

        output_filename = StringVar()
        output_filename.set("Average")
        avg_outputFilename_entry = Entry(self, bg = "white", bd = 5, \
                textvariable=output_filename, justify = LEFT, font=("Times", 12, "italic"))

        #Avg_Spectrum Button
        specificFiles_status = False
        allFiles_status = True
        avg_button = ttk.Button(self, text="Avg_spectrum")
        avg_button.config(command = lambda: avgSpec_plot(
                                                        i_avg_title.get(), \
                                                        i_avg_ts.get(), \
                                                        i_avg_lgs.get(), \
                                                        i_avg_minor.get(), \
                                                        i_avg_major.get(), \
                                                        i_avg_majorTick.get(), \
                                                        output_filename.get(),\
                                                        self.location,\
                                                        mname.get(), temp.get(), bwidth.get(), ie.get(),\
                                                        normavg_saveCheck_value.get(),\
                                                        specificFiles_status,\
                                                        allFiles_status,\
                                                        i_avg_xlabelsz.get(), i_avg_ylabelsz.get(),\
                                                        i_avg_fwidth.get(), i_avg_fheight.get(),\
                                                        i_avg_markersz.get(), norm_show_value.get(),\
                                                        delta.get(), self.filelist
                                                        )
                                                        )

        # Save checkbutton for normline and avgspec:
        normavg_saveCheck_value = BooleanVar()
        normavg_saveCheck_value.set(True)
        normavg_saveCheck = ttk.Checkbutton(self, text = "Save", variable = normavg_saveCheck_value)
        

        # Spectrum Analyzer and power Analyzer Buttons:
        sa_button = ttk.Button(self, text="SA", \
                command = lambda: FELion_Sa(self.fname, self.location))
        power_button = ttk.Button(self, text = "Power", \
                command = lambda: FELion_Power(self.fname, self.location))

        self.filelist = []
        def openfilelist(self):
                self.filelist = []
                self.openlist = askopenfilenames(self, initialdir=self.location, initialfile='tmp',
                                filetypes=[("Felix Files", "*.felix"), ("All files", "*")])
                
                for i in self.openlist:

                        location = i.split(os.sep)
                        
                        file = location[-1]
                        self.filelist.append(file)

                        del location[-1]
                        self.location = os.sep.join(location)
        
                filelist_label.config(text = '\n'.join(self.filelist))
                current_location.config(text = self.location)

                return self.filelist
                
        openfiles = ttk.Button(self, text = "Select File(s)", command = lambda: openfilelist(self))
        filelist_label = Label(self)

        
        norm_diff = 0.12
        norm_smalldiff = 0.06

        n_x1 = 0.1
        n_x2 = n_x1 + norm_diff
        n_x3 = n_x2 + norm_diff +0.05
        n_x4 = n_x3 + norm_diff
        n_x5 = n_x4 + norm_smalldiff
        n_x6 = n_x5 + norm_diff
        n_x7 = n_x6 + norm_smalldiff


        n_y1 = 0.1
        ynorm_diff = 0.1
        n_y2 = n_y1 + ynorm_diff
        n_y3 = n_y2 + ynorm_diff +0.05
        n_y4 = n_y3 + ynorm_diff
        n_y5 = n_y4 + ynorm_diff
        n_y6 = n_y5 + ynorm_diff


        browse_loc.place(relx = n_x1,  rely =n_y1, width = width, height = height)
        fname_label.place(relx = n_x1,  rely =n_y2, width = width, height = height)
        molecule_name_label.place(relx = n_x1,  rely = n_y3, width = width, height = height)
        temp_label.place(relx = n_x1,  rely = n_y4, width = width, height = height)
        bwidth_label.place(relx = n_x1,  rely =n_y5, width = width, height = height)
        ion_enrg_label.place(relx = n_x1,  rely = n_y6, width = width, height = height)

        current_location.place(relx = n_x2,  rely = n_y1, relwidth = 0.5, height = height)
        filename_label.place(relx = n_x2,  rely = n_y2, width = width, height = height)
        molecule_name.place(relx = n_x2,  rely = n_y3, width = width, height = height)
        temperature.place(relx = n_x2,  rely =n_y4, width = width, height = height)
        bo_Width.place(relx = n_x2,  rely = n_y5, width = width, height = height)
        ion_enrg.place(relx = n_x2,  rely =n_y6, width = width, height = height)

        
        a_y3 = n_y2 + ynorm_diff
        a_y4 = a_y3 + ynorm_diff
        a_y5 = a_y4 + ynorm_diff
        a_y6 = a_y5 + ynorm_diff
        a_y7 = a_y6 + ynorm_diff
        a_y8 = a_y7 + ynorm_diff


        avg_label.place(relx = n_x3,  rely = n_y2, relwidth = 0.2, height = 40)
        delta_label.place(relx = n_x6,  rely = n_y2, width = width, height = 40)
        delta_value.place(relx = n_x6+0.12,  rely = n_y2, width = width, height = 40)
        
        avg_title.place(relx = n_x3,  rely = a_y3, width = width, height = height)
        avg_ts_ls.place(relx = n_x3,  rely = a_y4, width = width, height = height)
        avg_xaxis_count.place(relx = n_x3,  rely = a_y5, width = width, height = height)
        avg_majorTick.place(relx = n_x3,  rely = a_y6, width = width, height = height)

        avg_title_Entry.place(relx = n_x4,  rely = a_y3, width = width, height = height)
        avg_ts_Entry.place(relx = n_x4,  rely = a_y4, width = smallwidth, height = height)
        avg_lgs_Entry.place(relx = n_x5,  rely = a_y4, width = smallwidth, height = height)
        avg_minor_Entry.place(relx = n_x4,  rely = a_y5, width = smallwidth, height = height)
        avg_major_Entry.place(relx = n_x5,  rely = a_y5, width = smallwidth, height = height)
        avg_majorTick_Entry.place(relx = n_x4,  rely = a_y6, width = smallwidth, height = height)
        avg_markersize_Entry.place(relx = n_x5,  rely = a_y6, width = smallwidth, height = height)

        avg_outputFilename.place(relx = n_x3,  rely =a_y7, width = width, height = height)
        avg_outputFilename_entry.place(relx = n_x4,  rely = a_y7, width = width, height = height)

        avg_xywf.place(relx = n_x3,  rely =a_y8, width = width, height = height)
        avg_xlabelsz.place(relx = n_x4,  rely =a_y8, width = smallwidth, height = height)
        avg_ylabelsz.place(relx = n_x5,  rely =a_y8, width = smallwidth, height = height)
        avg_fwidth.place(relx = n_x6-0.05,  rely =a_y8, width = smallwidth, height = height)
        avg_fheight.place(relx = n_x7-0.05,  rely =a_y8, width = smallwidth, height = height)

        normavg_saveCheck.place(relx = n_x6,  rely = a_y3, width = width, height = height)
        norm_show.place(relx = n_x6+0.15,  rely = a_y3, width = width, height = height)
        #normallCheck.place(relx = n_x6,  rely = a_y4, width = width+45, height = height)

        normline_button.place(relx = n_x6,  rely = a_y4, width = width, height = height)
        sa_button.place(relx = n_x6,  rely = a_y5, width = width, height = height)
        power_button.place(relx = n_x6,  rely = a_y6, width = width, height = height)
        
        openfiles.place(relx = n_x6+0.15,  rely = a_y4, width = width, height = height)
        avg_button.place(relx = n_x6+0.15,  rely = a_y5, width = width, height = height)
        filelist_label.place(relx = n_x6+0.15,  rely = a_y6)

class Mass(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")
        
        label = Label(self, text="Mass Spectrum", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Norm and Avg",
                            command=lambda: controller.show_frame(Normline))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Powerfile",
                            command=lambda: controller.show_frame(Powerfile))
        button3.place(relx = x3, rely = y, width = width, height = height)

        button4 = ttk.Button(self, text="Plot",
                            command=lambda: controller.show_frame(Plot))
        button4.place(relx = x4, rely = y, width = width, height = height)

        # Opening a Directory:
        self.location = "/"
        self.fname = ""

        def open_dir(self):

            root = Tk()
            root.withdraw()

            root.filename =  filedialog.askopenfilename(initialdir = self.location, title = "Select file", filetypes = (("Mass files","*.mass"),("all files","*.*")))
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
        
        self.filelist = []
        def openfilelist(self):
                self.filelist = []
                self.openlist = askopenfilenames(self, initialdir=self.location, initialfile='tmp',
                                filetypes=[("Mass files", "*.mass"), ("All files", "*")])
                
                for i in self.openlist:

                        location = i.split(os.sep)
                        
                        file = location[-1]
                        self.filelist.append(file)

                        del location[-1]
                        self.location = os.sep.join(location)
        
                filelist_label.config(text = '\n'.join(self.filelist))
                current_location.config(text = self.location)

                return self.filelist
                
        openfiles = ttk.Button(self, text = "Select File(s)", command = lambda: openfilelist(self))
        filelist_label = Label(self)

        # Printing current location:
        current_location = Label(self)
        filename_label = Label(self)

        massSpec_label = Label(self, text = "Mass_file: ", font=("Times", 10, "bold"))

        # the compund details:
        molecule_name_label = Label(self, text = "Molecule", font=("Times", 10, "bold"))
        temp_label = Label(self, text = "TEMP(K)", font=("Times", 10, "bold"))
        bwidth_label = Label(self, text = "B0 Width(ms)", font=("Times", 10, "bold"))
        ion_enrg_label = Label(self, text = "IE(eV)", font=("Times", 10, "bold"))

        mname = StringVar()
        temp = StringVar()
        bwidth = StringVar()
        ie = StringVar()

        mname.set("Molecule")
        temp.set("-")
        bwidth.set("-")
        ie.set("-")

        molecule_name = Entry(self, bg = "white", bd = 5, textvariable=mname, justify = LEFT, font=("Times", 12, "italic"))
        temperature = Entry(self, bg = "white", bd = 5, textvariable=temp, justify = LEFT, font=("Times", 12, "italic"))
        bo_Width = Entry(self, bg = "white", bd = 5, textvariable=bwidth, justify = LEFT, font=("Times", 12, "italic"))
        ion_enrg = Entry(self, bg = "white", bd = 5, textvariable=ie, justify = LEFT, font=("Times", 12, "italic"))
      
        mass_button = ttk.Button(self, text="MassSpec", \
                                        command = lambda: massSpec(\
                                        self.fname, mname.get(), temp.get(), bwidth.get(), ie.get(),\
                                        self.location,\
                                        self.filelist,\
                                        output_filename.get(),\
                                        mass_method_value.get(),\
                                        mass_saveCheck_value.get()
                                        )
                                )

        # Save checkbutton:
        mass_saveCheck_value = BooleanVar()
        mass_saveCheck_value.set(True)
        mass_saveCheck = ttk.Checkbutton(self, text = "Save", variable = mass_saveCheck_value)

        #Combine Mass spec:
        def combine_func(self, combine):
                if not combine:
                        display_label.config(text = "Single mode active:")
                if combine:
                        display_label.config(text = "Combine mode active:")
                        
                
        display_label = Label(self, font=("Times", 12, "italic"), bg = "sea green")
        
        mass_method_value = BooleanVar()
        single_mass = ttk.Radiobutton(self, text = "Single: ", \
                variable = mass_method_value, value = False, \
                command = lambda: combine_func(self, mass_method_value.get()))
        combine_mass = ttk.Radiobutton(self, text = "Combine: ", \
                variable = mass_method_value, value = True, \
                command = lambda: combine_func(self, mass_method_value.get()))

        # avg spectrum output filename:
        avg_outputFilename = Label(self, \
                text = "Output filename\n(Combine mode)", font=("Times", 10, "bold"))

        output_filename = StringVar()
        output_filename.set("Average")
        avg_outputFilename_entry = Entry(self, bg = "white", bd = 5, \
                textvariable=output_filename, justify = LEFT, font=("Times", 12, "italic"))

           
        mass_diff = 0.12
        mass_smalldiff = 0.06

        m_x1 = 0.1
        m_x2 = m_x1 + mass_diff
        m_x3 = m_x2 + mass_diff +0.05
        m_x4 = m_x3 + mass_diff
        m_x5 = m_x4 + mass_smalldiff
        m_x6 = m_x5 + mass_diff
        m_x7 = m_x6 + mass_diff

        m_y1 = 0.1
        ymass_diff = 0.1
        m_y2 = m_y1 + ymass_diff
        m_y3 = m_y2 + ymass_diff +0.05
        m_y4 = m_y3 + ymass_diff
        m_y5 = m_y4 + ymass_diff
        m_y6 = m_y5 + ymass_diff

        browse_loc.place(relx = m_x1,  rely =m_y1, width = width, height = height)
        massSpec_label.place(relx = m_x1,  rely =m_y2, width = width, height = height)
        molecule_name_label.place(relx = m_x1,  rely = m_y3, width = width, height = height)
        temp_label.place(relx = m_x1,  rely = m_y4, width = width, height = height)
        bwidth_label.place(relx = m_x1,  rely =m_y5, width = width, height = height)
        ion_enrg_label.place(relx = m_x1,  rely = m_y6, width = width, height = height)

        current_location.place(relx = m_x2,  rely = m_y1, relwidth = 0.5, height = height)
        filename_label.place(relx = m_x2,  rely = m_y2, width = width, height = height)
        molecule_name.place(relx = m_x2,  rely = m_y3, width = width, height = height)
        temperature.place(relx = m_x2,  rely =m_y4, width = width, height = height)
        bo_Width.place(relx = m_x2,  rely = m_y5, width = width, height = height)
        ion_enrg.place(relx = m_x2,  rely =m_y6, width = width, height = height)

        single_mass.place(relx = m_x4,  rely = m_y2, width = width, height = height)
        
        display_label.place(relx = m_x6+0.01,  rely = m_y1, relwidth = 0.25, height = height)

        mass_saveCheck.place(relx = m_x3,  rely = m_y2, width = width, height = height)
        mass_button.place(relx = m_x3+0.05,  rely = m_y3, width = width, height = height)

        avg_outputFilename.place(relx = m_x3,  rely = m_y6, width = width+30, height = height)
        avg_outputFilename_entry.place(relx = m_x4+0.05,  rely = m_y6, width = width, height = height)

        combine_mass.place(relx = m_x6+0.01,  rely = m_y2, width = width, height = height)
        openfiles.place(relx = m_x6+0.01,  rely = m_y3, width = width, height = height)
        filelist_label.place(relx = m_x6+0.01,  rely = m_y4)
        
class Powerfile(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")
        
        label = Label(self, text="Powerfile Generator", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Norm and Avg",
                            command=lambda: controller.show_frame(Normline))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Mass Spec",
                            command=lambda: controller.show_frame(Mass))
        button3.place(relx = x3, rely = y, width = width, height = height)

        button4 = ttk.Button(self, text="Plot",
                            command=lambda: controller.show_frame(Plot))
        button4.place(relx = x4, rely = y, width = width, height = height)

        # Labels and buttons:

        # Opening a Directory:
        self.location = "/"
        date = datetime.datetime.now()
        self.fname = date.strftime("%d_%m_%y-#")

        def open_dir(self):

            root = Tk()
            root.withdraw()

            root.directory =  filedialog.askdirectory()
            self.location = root.directory

            root.destroy()
            location_entry.config(text = self.location)
            return

        location_entry = Label(self)
  
        # Labels and buttons:
        location_label = ttk.Button(self, text = "Select Folder")
        location_label.config(command = lambda: open_dir(self))

        #Label for Entry Box;
        user_input_label = Label(self, text = "Filename:", font=("Times", 10, "bold"))

        #Entry Box;
        init_msg = self.fname #initialising message
        content = StringVar()   #defining Stringvar()
        user_input = Entry(self, bg = "white", bd = 5, textvariable=content, justify = LEFT)
        user_input.config(font=("Times", 12, "italic"))
        user_input.focus_set()
        content.set(init_msg)

        #Baseline
        save_button = ttk.Button(self, text="Save")
        save_button.config(command = lambda: outFile(content.get(), self.location, T.get("1.0", "end-1c")))

        T = Text(self)
        S = Scrollbar(self)
        T.config(yscrollcommand=S.set)
        S.config(command=T.yview)
        
        quote = """#POWER file\n# 10 Hz FELIX\n#\n#SHOTS=26\n#INTERP=linear\n#    IN_no_UM (if one deletes the "no" the firs number will be in \mu m\n# wavelength/cm-1      energy/pulse/mJ\n"""
        T.insert(END, quote)

        location_label.place(relx = 0.1,  rely = 0.1, width = 100, height = 40)
        location_entry.place(relx = 0.3,  rely = 0.1, relwidth = 0.5, height = 40)

        user_input_label.place(relx = 0.1,  rely = 0.3, width = 100, height = 40)
        user_input.place(relx = 0.3,  rely = 0.3, width = 100, height = 40)
        save_button.place(relx = 0.5,  rely = 0.3, width = 100, height = 40)

        T.place(relx = 0.15,  rely = 0.4, relwidth = 0.7, relheight = 0.4)
        S.place(relx = 0.85,  rely = 0.4, width = 15, relheight = 0.4)

class Plot(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent, bg="sea green")
        
        label = Label(self, text="Plot", \
                font=LARGE_FONT, bg="sea green", bd = 1, relief = SOLID)
        label.place(relx = 0, rely = 0, relwidth = 1)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Norm and Avg",
                            command=lambda: controller.show_frame(Normline))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Mass Spec",
                            command=lambda: controller.show_frame(Mass))
        button3.place(relx = x3, rely = y, width = width, height = height)

        button4 = ttk.Button(self, text="Powerfile",
                            command=lambda: controller.show_frame(Mass))
        button4.place(relx = x4, rely = y, width = width, height = height)


        def normalising(self, filename, combine, norm, show, log, save):
                try:
                        os.chdir(self.location)

                        def fopen(self, filename):
                                f = open(filename)
                                x, y, normy = [],[], []
                                for i in f:
                                        if not i[0] == "#" and not i == "\n":
                                                a, b = i.split()
                                                x.append(float(a))
                                                y.append(float(b))

                                # normalising (Feature Scaling (0,1) range):
                                for j in y:
                                        j = (j-min(y))/(max(y)-min(y))
                                        normy.append(j)
                                
                                f.close()
                                return x, y, normy

                        plt.grid(True)

                        if not combine:
                                x, y, normy = fopen(self, filename)
                                if norm:
                                        if log: plt.semilogy(x, normy, label = filename.split(".")[0])
                                        else:   plt.plot(x, normy, label = filename.split(".")[0])

                                else:
                                        if log: plt.semilogy(x,y, label = filename.split(".")[0])
                                        else:   plt.plot(x,y, label = filename.split(".")[0])

                        if combine:
                                filelist = self.filelist

                                for i in filelist:
                                        i = i.strip()
                                        x, y, normy = fopen(self, i)

                                        if norm:
                                                if log: plt.semilogy(x, normy, label = i.split(".")[0])
                                                else:   plt.plot(x, normy, label = i.split(".")[0])

                                        else:
                                                if log: plt.semilogy(x,y, label = i.split(".")[0])
                                                else:   plt.plot(x,y, label = i.split(".")[0])


                        plt.legend()
                        plt.xlabel("Wavenumber(cm-1)")

                        if norm:
                                plt.ylabel("Normalised (Scaled to 1) Intensity")
                        else:
                                plt.ylabel("Intensity")
                        
                        plt.tight_layout()

                        if save:
                                if combine:
                                        plt.savefig('combined.png')
                                        
                                else:
                                        plt.savefig(filename.split(".")[0]+".png")
                                        

                        if show:
                                plt.show()
                        
                        if save and combine:
                                ShowInfo("SAVED", "Filename: combined.png")
                        if save and not combine:
                                ShowInfo("SAVED:", "Filename: %s"%(filename.split(".")[0]+".png"))

                        plt.close()
                        return
                except Exception as e:
                        ErrorInfo("Error: ", e)

        # Opening a Directory:
        self.location = "/"
        self.fname = ""

        def open_dir(self):

            root = Tk()
            root.withdraw()

            root.filename =  filedialog.askopenfilename(initialdir = self.location, title = "Select file", filetypes = (("all files","*.*"), ("all files","*.*")))
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

        filename = Label(self, text = "Filename: ", font=("Times", 10, "bold"))

        normCheck_value = BooleanVar()
        normCheck_value.set(False)
        normCheck = ttk.Checkbutton(self, text = "Normalise", variable = normCheck_value)

        combineCheck_value = BooleanVar()
        combineCheck_value.set(False)
        combineCheck = ttk.Checkbutton(self, text = "Combine", variable = combineCheck_value)

        show_value = BooleanVar()
        show_value.set(True)
        show = ttk.Checkbutton(self, text = "Show", variable = show_value)

        log_value = BooleanVar()
        log_value.set(False)
        log = ttk.Checkbutton(self, text = "Log", variable = log_value)

        fit_value = BooleanVar()
        fit_value.set(True)
        fit = ttk.Checkbutton(self, text = "", variable = fit_value)


        # opening multiple files
        
        self.filelist = []
        def openfilelist(self):
                self.filelist = []
                self.openlist = askopenfilenames(self, initialdir=self.location, initialfile='tmp',
                                filetypes=[("All files", "*"), ("All files", "*")])
                
                for i in self.openlist:

                        location = i.split(os.sep)

                        file = location[-1]
                        self.filelist.append(file)

                        del location[-1]
                        self.location = os.sep.join(location)
        
                filelist_label.config(text = '\n'.join(self.filelist))
                current_location.config(text = self.location)

                return self.filelist
                
        openfiles = ttk.Button(self, text = "Select File(s)", command = lambda: openfilelist(self))
        filelist_label = Label(self)
        

        plotbutton = ttk.Button(self, text="Plot", \
                command = lambda: normalising(\
                self, self.fname, combineCheck_value.get(), \
                #self.filelist,\
                normCheck_value.get(), \
                show_value.get(), log_value.get(), save.get()\
                )
                )

        timescan_plotbutton = ttk.Button(self, text="TimeScan", \
                command = lambda: timescanplot(self.fname, self.location, deg.get(), fit_value.get()))

        ployfit_label = Label(self, text = "Polyfit deg:", font=("Times", 10, "bold"))

        deg = IntVar()
        deg.set(3)
        polyfit_entry = Entry(self, bg = "white", bd = 5, \
                textvariable = deg, justify = LEFT, font=("Times", 12, "italic"))

        # Save checkbutton:
        save = BooleanVar()
        save.set(True)
        save_check = ttk.Checkbutton(self, text = "Save", variable = save)


        mass_diff = 0.12
        mass_smalldiff = 0.06

        m_x1 = 0.1
        m_x2 = m_x1 + mass_diff
        m_x3 = m_x2 + mass_diff +0.05
        m_x4 = m_x3 + mass_diff
        m_x5 = m_x4 + mass_smalldiff
        m_x6 = m_x5 + mass_diff
        m_x7 = m_x6 + mass_diff

        m_y1 = 0.1
        ymass_diff = 0.1
        m_y2 = m_y1 + ymass_diff
        m_y3 = m_y2 + ymass_diff +0.05
        m_y4 = m_y3 + ymass_diff
        m_y5 = m_y4 + ymass_diff
        m_y6 = m_y5 + ymass_diff

        browse_loc.place(relx = m_x1,  rely =m_y1, width = width, height = height)
        filename.place(relx = m_x1,  rely =m_y2, width = width, height = height)
        current_location.place(relx = m_x2,  rely = m_y1, relwidth = 0.5, height = height)
        filename_label.place(relx = m_x2,  rely = m_y2, width = width, height = height)
        normCheck.place(relx = m_x3,  rely = m_y2, width = width, height = height)
        combineCheck.place(relx = m_x1,  rely = m_y3, width = width, height = height)
        plotbutton.place(relx = m_x4,  rely = m_y2, width = width, height = height)
        timescan_plotbutton.place(relx = m_x5+0.06,  rely = m_y2, width = width, height = height)

        show.place(relx = m_x4,  rely = m_y3, width = width, height = height)
        log.place(relx = m_x3,  rely = m_y3, width = width, height = height)
        
        ployfit_label.place(relx = m_x5+0.06,  rely = m_y3, width = width, height = height)
        polyfit_entry.place(relx = m_x6+0.06,  rely = m_y3, width = smallwidth, height = height)
        fit.place(relx = m_x7,  rely = m_y3, width = smallwidth, height = height)

        openfiles.place(relx = m_x1,  rely = m_y4, width = width, height = height)
        filelist_label.place(relx = m_x1,  rely = m_y5)
        save_check.place(relx = m_x3,  rely = m_y4, width = width, height = height)

#Closing Program
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()

###################################################################################################################################################
# Main Program

app = FELion()

icons_locations = "C:/FELion-GUI/software/"
app.protocol("WM_DELETE_WINDOW", on_closing)

shutdown = PhotoImage(file = join(icons_locations, "power.png"))
restarticon = PhotoImage(file = join(icons_locations, "restart.png"))

power = ttk.Button(app, image=shutdown, text = 'power', command = lambda: app.destroy())
restart = ttk.Button(app, image=restarticon, text = 'restart', command = lambda: os.execl(sys.executable, sys.executable, *sys.argv))

restart.place(relx = 0.95, rely = 0.05)
power.place(relx = 0.95, rely = 0.15)

app.mainloop()