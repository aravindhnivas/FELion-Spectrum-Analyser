#!/usr/bin/python3

## Imported Modules Informations

# tkinter modules
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.filedialog import askopenfilenames, askopenfilename

# Built-In modules
import os
from os.path import join
import shutil
import datetime

# Data analysis and plotting modules
import matplotlib.pyplot as plt
import numpy as np

# Custom function modules
from timescan_plot import timescanplot
from depletion_plot import depletionPlot
from just_plot import theory_exp, power_plot
from FELion_definitions import *

#FELion modules
from FELion_massSpec import massSpec
from FELion_avgSpec import avgSpec_plot
from FELion_normline import normline_correction, show_baseline
from FELion_power import FELion_Power
from FELion_sa import FELion_Sa

class FELion(Tk):
        
        def __init__(self, *args, **kwargs):

                Tk.__init__(self, *args, **kwargs)

                Tk.iconbitmap(self,default='C:/FELion-GUI/software/FELion_Icon.ico')
                Tk.wm_title(self, "FELion-Spectrum Analyser v.3.0")
                Tk.wm_geometry(self, "1000x600")
        
                container = Frame(self)
                container.pack(side="top", fill="both", expand = True)
                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)

                StatusBarFrame = Frame(self)
                StatusBarFrame.pack(side = "bottom", fill = "both", expand = False)

                statusBar_left_text = "Version 3.0"
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

        def open_dir(self, cnt, x, y, type_file):
                cnt.fname, cnt.location = cnt.widget.open_dir(type_file)
                cnt.full_name = join(cnt.location, cnt.fname)

                cnt.widget.labels(
                        cnt.location, x, y, 
                        bd = 0,
                        relwidth = 0.5, relheight = 0.06
                )

                cnt.widget.labels(
                        cnt.fname, x, y+0.1, 
                        bd = 0,
                        relwidth = 0.15, relheight = 0.06
                )

                cnt.res, cnt.b0, cnt.trap_ms = var_find(cnt.fname, cnt.location)
                cnt.bwidth.set(cnt.b0)
                cnt.trap.set(cnt.trap_ms)

        def openfilelist(self, cnt, x1, y1, x2, y2, type_file):
                cnt.filelist, cnt.location = cnt.widget.openfilelist(type_file)

                cnt.widget.labels(
                        cnt.location, 
                        x1, y1, 
                        bd = 0,
                        relwidth = 0.5, relheight = 0.06
                )
                        
                cnt.widget.labels(
                        '\n'.join(cnt.filelist), 
                        x2, y2, 
                        bd = 0,
                        relwidth = 0.15, relheight = 0.2
                )

        def init_labels(self, cnt):
                label1 = ('Molecule', 'TEMP(K)', 'B0 Width(ms)', 'IE(eV)', 'Trap(ms)')

                y_ = 0.34
                for i in label1:
                        cnt.widget.labels(i, 0.1, y_)
                        y_ += 0.1
                
                cnt.mname = Entry_widgets(cnt, 'Entry', 'Molecule', 0.25, 0.34, bd = 5)
                cnt.temp = Entry_widgets(cnt, 'Entry', 0, 0.25, 0.44, bd = 5)
                cnt.bwidth = Entry_widgets(cnt, 'Entry', 0, 0.25, 0.54, bd = 5)
                cnt.ie = Entry_widgets(cnt, 'Entry', 0, 0.25, 0.64, bd = 5)
                cnt.trap = Entry_widgets(cnt, 'Entry', 0, 0.25, 0.74, bd = 5)

        def __repr__(self):
                return 'FELion Tkinter Tk() Class'
    
class StartPage(Frame):

        def __init__(self, parent, controller):
                Frame.__init__(self,parent, bg="sea green")

                self.widget = FELion_widgets(self)

                self.widget.labels('Start Page', 0, 0.05, bg="sea green", font = LARGE_FONT, relwidth = 1, relheight = 0.05)

                pages = ('Norm and Avg', 'Mass Spec', 'Powerfile', 'Plot')
                pages_name = (Normline, Mass, Powerfile, Plot)

                x, y = 0.15, 0.9
                for name, pages_n in zip(pages, pages_name):
                        self.widget.buttons(name , x, y, controller.show_frame, pages_n)
                        x += 0.15
                self.widget.buttons('Update' , x+0.07, y, update,'')
                self.widget.labels(welcome_msg, 0.1, 0.5, bg="sea green", font = ("Verdana", 11, "italic"), bd = 0, relwidth = 0.8, relheight = 0.75)

class Normline(Frame):

        def __init__(self, parent, controller):
                Frame.__init__(self,parent, bg="sea green")
                self.location = "/"
                self.fname = ""
                self.filelist = []
                self.foravgshow = False
                self.b0 = 0
                self.trap = 0

                self.widget = FELion_widgets(self)

                self.widget.labels('Normline', 0, 0.05, bg="sea green", font = LARGE_FONT, relwidth = 1, relheight = 0.05)

                pages = ('Back to Home', 'Mass Spec', 'Powerfile', 'Plot')
                pages_name = (StartPage, Mass, Powerfile, Plot)

                x, y = 0.15, 0.9
                for name, pages_n in zip(pages, pages_name):
                        self.widget.buttons(name , x, y, controller.show_frame, pages_n)
                        x += 0.15

                self.widget.buttons('Browse' , 0.1, 0.1, controller.open_dir, self, 0.22, 0.14, felix_files_type)
                self.widget.labels('Filename', 0.1, 0.24)
                
                controller.init_labels(self)

                self.normavg_saveCheck_value = Entry_widgets(self, 'Check', 'Save', 0.7, 0.3, default = False)
                self.normallCheck_value = Entry_widgets(self, 'Check', 'Plot all', 0.7, 0.4, default = False)
                self.norm_show_value = Entry_widgets(self, 'Check', 'Show', 0.84, 0.3, default = True)

                
                self.widget.buttons('Normline' , 0.7, 0.5, self.Normline_func)
   
                # avg_labels's label:
                self.widget.labels('For Average Spectrum', 0.4, 0.24, bd = 2,  relwidth = 0.2)
                self.widget.labels('DELTA', 0.7, 0.24)
                self.delta = Entry_widgets(self, 'Entry', 2, 0.84, 0.24, bd = 5)

                # Avg_Spectrum Labels:
                label2 = ('Title', 'Size\n(Title,Legend)', 'X-axis\nticks div:', 'Major_TickSz,\nMarkerSz', 'Output', 'X,Y,Wid,Ht', )

                y_ = 0.34
                for i in label2:
                        self.widget.labels(i, 0.4, y_)
                        y_ += 0.1
                
                #Avg_Spectrum Button
                self.widget.buttons('Avg_spectrum' , 0.84, 0.5, self.Avg_spectrum_func)

                self.avg_title = Entry_widgets(self, 'Entry',  'Title' , 0.55, 0.34, bd = 2)
                self.avg_ts = Entry_widgets(self, 'Entry',  15 , 0.55, 0.44, bd = 2, relwidth = 0.05)
                self.avg_lgs = Entry_widgets(self, 'Entry',  10 , 0.6, 0.44, bd = 2, relwidth = 0.05)

                self.avg_minor = Entry_widgets(self, 'Entry',  20 , 0.55, 0.54, bd = 2, relwidth = 0.05)
                self.avg_major = Entry_widgets(self, 'Entry',  100 , 0.6, 0.54, bd = 2, relwidth = 0.05)

                self.avg_majorTick = Entry_widgets(self, 'Entry',  15 , 0.55, 0.64, bd = 2, relwidth = 0.05)
                self.avg_markersz = Entry_widgets(self, 'Entry',  2 , 0.6, 0.64, bd = 2, relwidth = 0.05)

                self.output_filename = Entry_widgets(self, 'Entry',  'Average' , 0.55, 0.74, bd = 2)
                
                self.avg_xlabelsz = Entry_widgets(self, 'Entry',  15 , 0.55, 0.84, bd = 2, relwidth = 0.05)
                self.avg_ylabelsz = Entry_widgets(self, 'Entry',  15 , 0.6, 0.84, bd = 2, relwidth = 0.05)
                self.avg_fwidth = Entry_widgets(self, 'Entry',  10 , 0.65, 0.84, bd = 2, relwidth = 0.05)
                self.avg_fheight = Entry_widgets(self, 'Entry',  5 , 0.7, 0.84, bd = 2, relwidth = 0.05)

                # Spectrum Analyzer and power Analyzer Buttons:
                self.widget.buttons('SA' , 0.7, 0.6, self.SA, relwidth = 0.05)
                self.widget.buttons('Power' , 0.75, 0.6, self.Power, relwidth = 0.05)
                self.widget.buttons('Baseline' , 0.7, 0.7, self.showBaseline)
                self.widget.buttons('Select File(s)' , 0.84, 0.4, controller.openfilelist, self, 0.22, 0.14, 0.84, 0.7, felix_files_type)

        def Normline_func(self):
                
                normline_correction(
                        self.fname, self.location,
                        self.mname.get(), self.temp.get(), self.bwidth.get(), self.ie.get(),
                        self.normavg_saveCheck_value.get(),
                        self.foravgshow, self.normallCheck_value.get(), self.filelist, self.norm_show_value.get()
                )
        
        def Avg_spectrum_func(self):
                avgSpec_plot(
                        self.avg_title.get(), self.avg_ts.get(), self.avg_lgs.get(), self.avg_minor.get(), 
                        self.avg_major.get(), self.avg_majorTick.get(), self.avg_markersz.get(),
                        self.avg_xlabelsz.get(), self.avg_ylabelsz.get(), self.avg_fwidth.get(), self.avg_fheight.get(), self.output_filename.get(),
                        self.location, self.mname.get(), self.temp.get(), self.bwidth.get(), self.ie.get(),
                        self.normavg_saveCheck_value.get(), self.norm_show_value.get(), self.delta.get(), self.filelist
                )

        def SA(self):
                FELion_Sa(self.fname, self.location)
        def Power(self):
                FELion_Power(self.fname, self.location)
        def showBaseline(self):
                show_baseline(self.fname, self.location, self.mname.get())

class Mass(Frame):

        def __init__(self, parent, controller):
                Frame.__init__(self,parent, bg="sea green")
                self.widget = FELion_widgets(self)

                self.widget.labels('Mass Spectrum', 0, 0.05, bg="sea green", font = LARGE_FONT, relwidth = 1, relheight = 0.05)

                pages = ('Back to Home', 'Norm and Avg', 'Powerfile', 'Plot')
                pages_name = (StartPage, Normline, Powerfile, Plot)

                x, y = 0.15, 0.9
                for name, pages_n in zip(pages, pages_name):
                        self.widget.buttons(name , x, y, controller.show_frame, pages_n)
                        x += 0.15

                self.widget.buttons('Browse' , 0.1, 0.1, controller.open_dir, self, 0.22, 0.14, mass_files_type)
                self.widget.labels('Mass File', 0.1, 0.24)

                self.location = "/"
                self.fname = ""
                self.filelist = []

                controller.init_labels(self)

                self.save = Entry_widgets(self, 'Check', 'Save', 0.4, 0.2, default = False)
                self.combine = Entry_widgets(self, 'Check', 'Combine', 0.6, 0.2, default = False)

                self.widget.buttons('Select File(s)' , 0.75, 0.2, controller.openfilelist, self, 0.22, 0.14, 0.84, 0.7, mass_files_type)

                self.widget.labels('Output', 0.6, 0.3)
                self.output_filename = Entry_widgets(self, 'Entry',  'Average' , 0.75, 0.3, bd = 2)

                self.widget.buttons('Mass Spec' , 0.5, 0.5, self.MassSpec_func)

        def MassSpec_func(self):
                massSpec(
                        self.fname, self.location,
                        self.mname.get(), self.temp.get(), self.bwidth.get(), self.ie.get(),
                        self.filelist, self.output_filename.get(), self.combine.get(), self.save.get()
                )
       
class Powerfile(Frame):

        def __init__(self, parent, controller):
                Frame.__init__(self,parent, bg="sea green")

                self.widget = FELion_widgets(self)

                self.widget.labels('Powerfile Generator', 0, 0.05, bg="sea green", font = LARGE_FONT, relwidth = 1, relheight = 0.05)

                pages = ('Back to Home', 'Norm and Avg', 'Mass Spec', 'Plot')
                pages_name = (StartPage, Normline, Mass, Plot)

                x, y = 0.15, 0.9
                for name, pages_n in zip(pages, pages_name):
                        self.widget.buttons(name , x, y, controller.show_frame, pages_n)
                        x += 0.15

                self.location = "/"
                self.date = datetime.datetime.now().strftime("%d_%m_%y-#")

                self.widget.buttons('Select Folder' , 0.1, 0.1, self.open_full_dir, 0.22, 0.14)
                self.widget.labels('Filename:', 0.1, 0.3)

                self.filename = Entry_widgets(self, 'Entry', self.date, 0.3, 0.3, bd = 5)

                self.quote = """#POWER file\n# 10 Hz FELIX\n#\n#SHOTS=26\n#INTERP=linear\n#    IN_no_UM (if one deletes the "no" the firs number will be in \mu m\n# wavelength/cm-1      energy/pulse/mJ\n"""
                self.power = Entry_widgets(self, 'power_box', self.quote, 0.15, 0.4)

                self.widget.buttons('Save' , 0.5, 0.3, self.power_box)
      
        def open_full_dir(self, x, y):
                self.location = self.widget.open_full_dir()

                self.widget.labels(
                        self.location, x, y, 
                        bd = 0,
                        relwidth = 0.5, relheight = 0.06
                )
                
        def power_box(self):
                outFile(self.filename.get(), self.location, self.power.power_get())

class Plot(Frame):

        def __init__(self, parent, controller):
                Frame.__init__(self,parent, bg="sea green")

                self.widget = FELion_widgets(self)

                self.widget.labels('Plot', 0, 0.05, bg="sea green", font = LARGE_FONT, relwidth = 1, relheight = 0.05)

                pages = ('Back to Home', 'Norm and Avg', 'Mass Spec', 'Powerfile')
                pages_name = (StartPage, Normline, Mass, Powerfile)

                x, y = 0.15, 0.9
                for name, pages_n in zip(pages, pages_name):
                        self.widget.buttons(name , x, y, controller.show_frame, pages_n)
                        x += 0.15
        
                self.widget.buttons('Browse' , 0.1, 0.1, controller.open_dir, self, 0.22, 0.14, all_files_type)
                self.widget.labels('Filename', 0.1, 0.24)

                self.location = "/"
                self.fname = ""
                self.filelist = []
                self.full_name = ''

                self.widget.buttons('Select File(s)' , 0.1, 0.34, controller.openfilelist, self, 0.22, 0.14, 0.1, 0.55, all_files_type)
                self.save = Entry_widgets(self, 'Check', 'Save', 0.4, 0.2, default = False)
                self.show = Entry_widgets(self, 'Check', 'Show', 0.52, 0.2, default = True)

                self.widget.buttons('Timescan' , 0.4, 0.3, self.timescan_func)
                self.widget.buttons('Depletion' , 0.52, 0.3, self.depletion_func)
                self.depletion_power = Entry_widgets(self, 'Entry',  'power_on, power_off, n_shots' , 0.52, 0.4, bd = 5, relwidth = 0.25)

                self.widget.labels('Select Exp. file using Browse and theory file (max 2) from Select file(s)', 0.4, 0.5, bd = 2, relwidth = 0.5)
                self.widget.buttons('Exp-Theory' , 0.4, 0.55, self.theory_func)

                self.widget.buttons('PowerPlot' , 0.65, 0.3, self.powerplot_func)


        def timescan_func(self):
                timescanplot(
                        self.fname, self.location, self.save.get(), self.show.get()
                )
        def depletion_func(self):
                depletionPlot(
                        self.filelist, self.location, self.save.get(), self.show.get(), self.depletion_power.get()
                )
        def theory_func(self):
                theory_exp(
                        self.filelist, self.full_name, self.location, self.save.get(), self.show.get()
                )
        def powerplot_func(self):
                power_plot(
                        self.filelist, self.location, self.save.get(), self.show.get()
                )

#Closing Program
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()

###################################################################################################################################################

app = FELion()

icons_locations = "C:/FELion-GUI/software/"
app.protocol("WM_DELETE_WINDOW", on_closing)

shutdown = PhotoImage(file = join(icons_locations, "power.png"))
restarticon = PhotoImage(file = join(icons_locations, "restart.png"))

power = ttk.Button(app, image = shutdown, text = 'power', command = lambda: app.destroy())
restart = ttk.Button(app, image = restarticon, text = 'restart', command = lambda: os.execl(sys.executable, sys.executable, *sys.argv))

restart.place(relx = 0.95, rely = 0.05)
power.place(relx = 0.95, rely = 0.15)

app.mainloop()

###################################################################################################################################################