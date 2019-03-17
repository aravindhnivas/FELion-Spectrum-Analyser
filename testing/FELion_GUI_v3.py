#!/usr/bin/python3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import datetime
import matplotlib.pyplot as plt

from timescan_plot import timescanplot
from depletion_plot import depletionPlot

#FELion modules
from FELion_massSpec import massSpec
from FELion_avgSpec import avgSpec_plot
from FELion_normline import normline_correction, show_baseline
from FELion_power import FELion_Power
from FELion_sa import FELion_Sa
from FELion_definitions import *

from tkinter.filedialog import askopenfilenames, askopenfilename
from os.path import join

import numpy as np

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

x = 0.15
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

                self.widget = FELion_widgets(self)

                self.widget.labels('Start Page', 0, 0.05, font = LARGE_FONT, relwidth = 1, relheight = 0.05)

                pages = ('Norm and Avg', 'Mass Spec', 'Powerfile', 'Plot')
                pages_name = (Normline, Mass, Powerfile, Plot)

                x = 0.15
                for name, pages_n in zip(pages, pages_name):
                        self.widget.buttons(name , x, y, controller.show_frame, pages_n, relwidth = 0.1, relheight = 0.06)
                        x += 0.15
                self.widget.buttons('Update' , x+0.07, y, update,'', relwidth = 0.1, relheight = 0.06)
                self.widget.labels(welcome_msg, 0.1, 0.5, font = ("Verdana", 11, "italic"), bd = 0, relwidth = 0.8, relheight = 0.75)

class Normline(Frame):

        def __init__(self, parent, controller):
                Frame.__init__(self,parent, bg="sea green")
                self.widget = FELion_widgets(self)

                self.location = "/"
                self.fname = ""
                self.filelist = []

                self.widget.labels('Normline', 0, 0.05, font = LARGE_FONT, bd = 1, relwidth = 1, relheight = 0.05)

                pages = ('Back to Home', 'Mass Spec', 'Powerfile', 'Plot')
                pages_name = (StartPage, Mass, Powerfile, Plot)

                x = 0.15
                for name, pages_n in zip(pages, pages_name):
                        self.widget.buttons(name , x, y, controller.show_frame, pages_n, relwidth = 0.1, relheight = 0.06)
                        x += 0.15

                self.widget.buttons('Browse' , 0.1, 0.1, self.open_dir, relwidth = 0.1, relheight = 0.06)
                self.widget.labels('Filename', 0.1, 0.24, bg = 'white', relwidth = 0.1, relheight = 0.06)

                label1 = ('Molecule', 'TEMP(K)', 'B0 Width(ms)', 'IE(eV)')
                entry1 = {
                        'mname':'Molecule', 
                        'temp':'-', 
                        'bwidth':'-', 
                        'ie':'-'
                }

                y_ = 0.34
                for i, e in zip(label1, entry1):
                        self.widget.labels(i, 0.1, y_, bg = 'white', relwidth = 0.1, relheight = 0.06)
                        entry1[e] = Entry_widgets(self, 'Entry',  entry1[e] , 0.25, y_, bg = 'White', bd = 5,
                                                relwidth = 0.1, relheight = 0.06)
                        y_ += 0.1
                self.mname, self.temp, self.bwidth, self.ie = entry1['mname'].get(), entry1['temp'].get(), entry1['bwidth'].get(), entry1['ie'].get()

                self.normavg_saveCheck_value = Entry_widgets(self, 'Check', 'Save', 0.7, 0.3, default = False, relwidth = 0.1, relheight = 0.06)
                self.normallCheck_value = Entry_widgets(self, 'Check', 'Plot all', 0.7, 0.4, default = False, relwidth = 0.1, relheight = 0.06)
                self.norm_show_value = Entry_widgets(self, 'Check', 'Show', 0.84, 0.3, default = True, relwidth = 0.1, relheight = 0.06)

                self.foravgshow = False
                self.widget.buttons('Normline' , 0.7, 0.5, self.Normline_func, relwidth = 0.1, relheight = 0.06)
   
                # avg_labels's label:
                self.widget.labels('For Average Spectrum', 0.4, 0.24, bg = 'white', bd = 2,  relwidth = 0.2, relheight = 0.06)
                self.widget.labels('DELTA', 0.7, 0.24, bg = 'white', relwidth = 0.1, relheight = 0.06)
                self.delta = Entry_widgets(self, 'Entry', 2, 0.84, 0.24, bg = 'White', bd = 5, relwidth = 0.1, relheight = 0.06)

                # Avg_Spectrum Labels:
                label2 = ('Title', 'Size\n(Title,Legend)', 'X-axis\nticks div:', 'Major_TickSz,\nMarkerSz', 'X,Y,Wid,Ht', 'Output')
                entry2 = {
                        'title':'Title', 
                        'Size_title_legend': '15, 10', 
                        'X-axis_ticks': '20, 100', 
                        'Major_ticks': '15, 2', 
                        'x,y,w,h': '15, 15, 10, 5',
                        'Output' : 'Average'
                }

                y_ = 0.34
                for i, e in zip(label2, entry2):
                        self.widget.labels(i, 0.4, y_, bg = 'white', relwidth = 0.1, relheight = 0.06)
                        entry2[e] = Entry_widgets(self, 'Entry',  entry2[e] , 0.55, y_, bg = 'White', bd = 5,
                                                relwidth = 0.1, relheight = 0.06)
                        y_ += 0.1


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
                                                                self.delta.get(), self.filelist
                                                                )
                                                                )

                # Spectrum Analyzer and power Analyzer Buttons:
                sa_button = ttk.Button(self, text="SA", \
                        command = lambda: FELion_Sa(self.fname, self.location))
                power_button = ttk.Button(self, text = "Power", \
                        command = lambda: FELion_Power(self.fname, self.location))

                baseline = ttk.Button(self, text="Baseline", \
                        command = lambda: show_baseline(self.fname, self.location, mname.get()))

                
                        
                openfiles = ttk.Button(self, text = "Select File(s)", command = lambda: self.openfilelist())
                filelist_label = Label(self)

                self.trap_time, self.B0_width = float(), int()
                def trap_time(self):
                        with open(join(self.location,self.fname), 'r') as f:
                                info = f.readlines()
                        filename = np.genfromtxt(info)
                        x, y = filename[:,0], filename[:,2]
                        self.range_min = x.min()
                        self.range_max = x.max()
                        self.count = y.max()
                        self.trap_time = [info[-21].split('#')[3].strip(),\
                                int(info[-21].split('#')[4].strip())/1000000]
                        self.B0_width = [info[-46].split('#')[3].strip(),\
                                int(int(info[-46].split('#')[4].strip())/1000)]
                        
                        trap_width_label.config(\
                                text = 'Trap: %.2f\tB0: %i\nRange: [%i, %i]\ncounts: %i'\
                                        %(self.trap_time[-1], self.B0_width[-1],\
                                        self.range_min,self.range_max, self.count)
                                        )
                        bwidth.set(self.B0_width[-1])
                
                trap_width_label = Label(self)

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

               
                trap_width_label.place(relx = n_x1,  rely = n_y6+0.1)

                a_y3 = n_y2 + ynorm_diff
                a_y4 = a_y3 + ynorm_diff
                a_y5 = a_y4 + ynorm_diff
                a_y6 = a_y5 + ynorm_diff
                a_y7 = a_y6 + ynorm_diff
                a_y8 = a_y7 + ynorm_diff

                sa_button.place(relx = n_x6,  rely = a_y6, width = 30, height = height)
                power_button.place(relx = n_x6+0.05,  rely = a_y6, width = 50, height = height)
                baseline.place(relx = n_x6,  rely = a_y7, width = width, height = height)
                
                openfiles.place(relx = n_x6+0.15,  rely = a_y4, width = width, height = height)
                avg_button.place(relx = n_x6+0.15,  rely = a_y5, width = width, height = height)
                filelist_label.place(relx = n_x6+0.15,  rely = a_y6)

        def open_dir(self):
                self.fname, self.location = self.widget.open_dir(felix_files_type)

                self.widget.labels(self.location, 0.22, 0.14, 
                        bd = 0, bg = 'white',
                        relwidth = 0.5, relheight = 0.06)
                self.widget.labels(self.fname, 0.22, 0.24, 
                        bd = 0, bg = 'white',
                        relwidth = 0.15, relheight = 0.06)

                #self.filename_label.config(text = self.fname)
                #if not self.fname=="" and not normallCheck_value.get(): trap_time(self)
   
        def openfilelist(self):
                self.filelist = []
                self.openlist = askopenfilenames(initialdir=self.location, initialfile='tmp',
                                filetypes=[("Felix Files", "*.felix"), ("All files", "*")])
                
                for i in self.openlist:

                        location = i.split("/")
                        
                        file = location[-1]
                        self.filelist.append(file)

                        del location[-1]
                        self.location = "/".join(location)
        
                filelist_label.config(text = '\n'.join(self.filelist))
                current_location.config(text = self.location)

                return self.filelist

        def Normline_func(self):
                
                normline_correction(
                        self.fname, self.location,
                        self.mname, self.temp, self.bwidth, self.ie,
                        self.normavg_saveCheck_value.get(),
                        self.foravgshow, self.normallCheck_value.get(), self.filelist, self.norm_show_value.get()
                        )


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
                self.openlist = askopenfilenames(initialdir=self.location, initialfile='tmp',
                                filetypes=[("Mass files", "*.mass"), ("All files", "*")])
                
                for i in self.openlist:

                        location = i.split("/")
                        
                        file = location[-1]
                        self.filelist.append(file)

                        del location[-1]
                        self.location = "/".join(location)
        
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
                                data = np.genfromtxt(filename)
                                x, y = data[:,0], data[:,1]
                                normy = (y-min(y))/(max(y)-min(y))
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
                                                else:   plt.plot(x, normy,".-", label = i.split(".")[0])

                                        else:
                                                if log: plt.semilogy(x,y, label = i.split(".")[0])
                                                else:   plt.plot(x,y,".-", label = i.split(".")[0])


                        plt.legend()
                        plt.xlabel("Wavenumber(cm-1)")

                        if norm:
                                plt.ylabel("Normalised (Scaled to 1) Intensity")

                        elif not combine and filename.split(".")[-1] == "pow":
                                plt.ylabel("Power (mJ)")
                        
                        elif combine and filelist[0].split(".")[-1] == "pow":
                                plt.ylabel("Power (mJ)")

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
        self.filename = ""

        def open_dir(self):

            root = Tk()
            root.withdraw()

            root.filename =  filedialog.askopenfilename(initialdir = self.location, title = "Select file", filetypes = (("all files","*.*"), ("all files","*.*")))
            filename, self.filename = root.filename, root.filename
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

        # opening multiple files
        
        self.filelist = []
        def openfilelist(self):
                self.filelist = []
                self.openlist = askopenfilenames(initialdir=self.location, initialfile='tmp',
                                filetypes=[("All files", "*"), ("All files", "*")])
                
                for i in self.openlist:

                        location = i.split("/")

                        file = location[-1]
                        self.filelist.append(file)

                        del location[-1]
                        self.location = "/".join(location)
        
                filelist_label.config(text = '\n'.join(self.filelist))
                current_location.config(text = self.location)

                return self.filelist, self.location
                
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
                command = lambda: timescanplot(self.fname, self.location, save.get(), show_value.get()))

        # Save checkbutton:
        save = BooleanVar()
        save.set(True)
        save_check = ttk.Checkbutton(self, text = "Save", variable = save)

        theory = ttk.Button(self, text = 'Theory_File',\
                command = lambda: theory_exp(\
                        self.filelist,\
                        self.filename, \
                        self.location, save.get(), show_value.get()))
        
        powerplot = ttk.Button(self, text='PowerPlot', command = lambda: power_plot(self.filelist, self.location, save.get(), show_value.get()))

        # depletion plot power and n values:
        power_n_value = StringVar()
        power_n_value.set('power_on, power_of, n_shots')
        power_n = Entry(self, bg = "white", bd = 5, textvariable=power_n_value, justify = LEFT, font=("Times", 12, "italic"))

        depletion_btn = ttk.Button(self, text='DepletionPlot', command = lambda: depletionPlot(self.filelist, self.location, save.get(), show_value.get(), power_n_value.get()))
        
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
        theory.place(relx = m_x5+0.06+0.12,  rely = m_y2, width = width, height = height)

        show.place(relx = m_x4,  rely = m_y3, width = width, height = height)
        log.place(relx = m_x3,  rely = m_y3, width = width, height = height)

        depletion_btn.place(relx = m_x5+0.06,  rely = m_y3, width = width, height = height)
        power_n.place(relx = m_x5+0.06+0.12,  rely = m_y3, width = width, height = height)
 
        openfiles.place(relx = m_x1,  rely = m_y4, width = width, height = height)
        filelist_label.place(relx = m_x1,  rely = m_y5)
        save_check.place(relx = m_x3,  rely = m_y4, width = width, height = height)
        powerplot.place(relx = m_x3,  rely = m_y5, width = width, height = height)

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