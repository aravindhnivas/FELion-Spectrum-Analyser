#!/usr/bin/python3

# tkinter modules
from tkinter import Frame, Label, SUNKEN, PhotoImage, ttk, messagebox

# Built-In modules
import os
from os.path import join, isfile, isdir
import datetime

# Custom function modules
from timescan_plot import timescanplot
from depletion_plot import depletionPlot
from just_plot import power_plot, plot, exp_theory
from kinetics import kinetics
from FELion_definitions import *

# FELion modules
from FELion_massSpec import massSpec
from FELion_avgSpec import avgSpec_plot
from FELion_normline import normline_correction
from FELion_power import FELion_Power
from FELion_sa import FELion_Sa
from FELion_baseline import baseline_correction, livePlot


try:
    # Make the window not to change the scale of this tkinter dpi application
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(0)
    print("Dpi awarness turned off")

except Exception:
    print("Dpi awarness cannot be turned off")

__version__ = "3.1.0"
print(f"\nFELion Spectrum Analyser {__version__}\n")
################################################# MODULES IMPORTED #################################################
####################################################################################################################

class FELion(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        Tk.iconbitmap(self, default='C:/FELion-GUI/software/FELion_Icon.ico')
        Tk.wm_title(self, "FELion-Spectrum Analyser v.3.0")
        Tk.wm_geometry(self, "1000x600")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.StatusBarFrame = Frame(self)
        self.StatusBarFrame.pack(side="bottom", fill="both", expand=False)

        self.statusBar_left_text = "Version 3.0"
        self.statusBar_left = Label(self.StatusBarFrame)
        self.statusBar_left.config(text=self.statusBar_left_text,
                                   relief=SUNKEN, bd=2, font="Times 10 italic", pady=5, anchor="w")
        self.statusBar_left.pack(side="top", fill="both", expand=True)

        self.statusBar_right_text = "Developed at dr. Sandra's Lab FELIX"
        self.statusBar_right = Label(self.StatusBarFrame)
        self.statusBar_right.config(text=self.statusBar_right_text,
                                    relief=SUNKEN, bd=2, font="Times 10 italic", pady=5, anchor="e")
        self.statusBar_right.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (StartPage, Normline, Mass, Powerfile, Plot):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def open_dir(self, cnt, type_file):
        cnt.fname, cnt.location = cnt.widget.open_dir(type_file)
        cnt.full_name = join(cnt.location, cnt.fname)

        if hasattr(cnt, 'location_label'):
            cnt.location_label.config(text=cnt.location)
        if hasattr(cnt, 'fname_label'):
            cnt.fname_label.config(text=cnt.fname)

        if hasattr(cnt, 'bwidth'):
            cnt.res, cnt.b0, cnt.trap_ms = var_find(cnt.fname, cnt.location)
            cnt.bwidth.set(cnt.b0)
            cnt.trap.set(cnt.trap_ms)

    def openfilelist(self, cnt, type_file):
        cnt.filelist, cnt.location = cnt.widget.openfilelist(type_file)

        if hasattr(cnt, 'location_label'):
            cnt.location_label.config(text=cnt.location)
        if hasattr(cnt, 'flist_label'):
            cnt.flist_label.config(text='\n'.join(cnt.filelist))

    def init_labels(self, cnt):
        label1 = ('Molecule', 'TEMP(K)', 'B0 Width(ms)',
                  'IE(eV)', 'Trap(ms)', 'DPI')
        label2 = ('Title', 'Size\n(Title,Legend)', 'X-axis\nticks div:',
                  'Major_TickSz,\nMarkerSz', 'Output', 'X,Y,Wid,Ht', )
        y_ = 0.34
        for i, j in zip(label1, label2):
            cnt.widget.labels(i, 0.1, y_)
            cnt.widget.labels(j, 0.4, y_)
            y_ += 0.1

        cnt.mname = cnt.widget.entries('Entry', 'Molecule', 0.25, 0.34, bd=5, help='Molecule Name')
        cnt.temp = cnt.widget.entries('Entry', 0, 0.25, 0.44, bd=5, help='Experiment temperature in Kelvin')
        cnt.bwidth = cnt.widget.entries('Entry', 0, 0.25, 0.54, bd=5, help='Automatically set from file')
        cnt.ie = cnt.widget.entries('Entry', 0, 0.25, 0.64, bd=5, help='Experiment Ionisation Energy')
        cnt.trap = cnt.widget.entries('Entry', 0, 0.25, 0.74, bd=5, help='Automatically set from file')
        cnt.dpi = cnt.widget.entries('Entry', 100, 0.25, 0.84, bd=5, help='Figure DPI')

        cnt.avg_title = cnt.widget.entries('Entry',  'Title', 0.55, 0.34, bd=2)
        cnt.avg_ts = cnt.widget.entries(
            'Entry',  15, 0.55, 0.44, bd=2, relwidth=0.05, help='Figure title fontsize')
        cnt.avg_lgs = cnt.widget.entries(
            'Entry',  10, 0.6, 0.44, bd=2, relwidth=0.05, help='Figure legend fontsize')

        cnt.avg_minor = cnt.widget.entries(
            'Entry',  20, 0.55, 0.54, bd=2, relwidth=0.05, help='X-axis tick mark scale position')
        cnt.avg_major = cnt.widget.entries(
            'Entry',  100, 0.6, 0.54, bd=2, relwidth=0.05, help='X-axis tick label scale position')

        cnt.avg_majorTick = cnt.widget.entries(
            'Entry',  15, 0.55, 0.64, bd=2, relwidth=0.05, help='X/Y Major tick label fontsize')
        cnt.avg_markersz = cnt.widget.entries(
            'Entry',  2, 0.6, 0.64, bd=2, relwidth=0.05, help='Scatter points fontsize (for average spectrum only)')

        cnt.output_filename = cnt.widget.entries(
            'Entry',  'Average', 0.55, 0.74, bd=2)

        cnt.avg_xlabelsz = cnt.widget.entries(
            'Entry',  15, 0.55, 0.84, bd=2, relwidth=0.05, help='X-label fontsize')
        cnt.avg_ylabelsz = cnt.widget.entries(
            'Entry',  15, 0.6, 0.84, bd=2, relwidth=0.05, help='Y-label fontsize')
        cnt.avg_fwidth = cnt.widget.entries(
            'Entry',  10, 0.65, 0.84, bd=2, relwidth=0.05, help='Figure width')
        cnt.avg_fheight = cnt.widget.entries(
            'Entry',  5, 0.7, 0.84, bd=2, relwidth=0.05,help='Figure height')

    def __repr__(self):
        return 'FELion Tkinter Tk() Class'


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="sea green")

        self.widget = FELion_widgets(self)

        self.widget.labels('Start Page', 0, 0.05, bg="sea green",
                           font=LARGE_FONT, relwidth=1, relheight=0.05)

        pages = ('Norm and Avg', 'Mass Spec', 'Powerfile', 'Plot')
        pages_name = (Normline, Mass, Powerfile, Plot)

        x, y = 0.15, 0.9
        for name, pages_n in zip(pages, pages_name):
            self.widget.buttons(name, x, y, controller.show_frame, pages_n)
            x += 0.15
        self.widget.buttons('Update', x+0.07, y, update, '')
        self.widget.labels(welcome_msg, 0.1, 0.5, bg="sea green", font=(
            "Verdana", 11, "italic"), bd=0, relwidth=0.8, relheight=0.75)


class Normline(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="sea green")

        normline_attributes = {
            'parent': parent, 'location': '/', 'fname': '', 'filelist': [], 'foravgshow': False,
            'b0': None, 'trap': None, 'mname': None, 'temp': None, 'bwidth': None, 'ie': None, 'dpi': None
        }

        for attr, values in normline_attributes.items():
            setattr(self, attr, values)

        self.widget = FELion_widgets(self, cnt=controller)

        self.widget.labels('Normline', 0, 0.05, bg="sea green",
                           font=LARGE_FONT, relwidth=1, relheight=0.05)

        pages = ('Back to Home', 'Mass Spec', 'Powerfile', 'Plot')
        pages_name = (StartPage, Mass, Powerfile, Plot)

        x, y = 0.15, 0.9
        for name, pages_n in zip(pages, pages_name):
            self.widget.buttons(name, x, y, controller.show_frame, pages_n)
            x += 0.15

        self.widget.labels('Filename', 0.1, 0.24)

        controller.init_labels(self)

        # BUTTONS

        # Function buttons
        self.widget.buttons('Baseline', 0.7, 0.3, self.Baseline)
        self.widget.buttons('Normline', 0.7, 0.5, self.Normline_func,
                            help='To look at the Complete Normalised Spectrum')
        self.widget.buttons('Avg_spectrum', 0.84, 0.3, self.Avg_spectrum_func,
                            help='Select multiple files using Slect File(s)')
        self.widget.buttons('SA', 0.7, 0.4, self.SA, relwidth=0.05)
        self.widget.buttons('Power', 0.75, 0.4, self.Power, relwidth=0.05)
        self.widget.buttons('LivePlot', 0.7, 0.6, self.LivePlot,
                            help='Interactive Plot: Baseline Correction --> Normalised Spectrum')

        # Other buttons
        self.widget.buttons('Select File(s)', 0.84, 0.4,
                            controller.openfilelist, self, felix_files_type)
        self.widget.buttons('Browse', 0.1, 0.1,
                            controller.open_dir, self, felix_files_type)

        # LABELS
        self.widget.labels('For Average Spectrum', 0.4,
                           0.24, bd=2,  relwidth=0.2)
        self.widget.labels('DELTA', 0.7, 0.24)
        self.location_label = self.widget.labels(
            self.location, 0.22, 0.14, bd=0, relwidth=0.7, relheight=0.06)
        self.fname_label = self.widget.labels(
            self.fname, 0.22, 0.24, bd=0, relwidth=0.15, relheight=0.06)
        self.flist_label = self.widget.labels(
            'Filelists', 0.84, 0.7, bd=0, relwidth=0.15, relheight=0.2)

        # Entries
        self.delta = self.widget.entries('Entry', 2, 0.84, 0.24, bd=5)
        self.hd = self.widget.entries('Check','HD', 0.82, 0.5, relwidth=0.05, help='Renders very high quality pdf and png using LATEX: But SLOW')

    def Normline_func(self):

        normline_correction(
            self.fname, self.location, self.mname.get(), self.temp.get(), self.bwidth.get(
            ), self.ie.get(), self.foravgshow, self.dpi.get(), self.parent, hd=self.hd.get(), trap=self.trap.get()
        )

    def Avg_spectrum_func(self):
        avgSpec_plot(
            self.avg_title.get(), self.avg_ts.get(), self.avg_lgs.get(), self.avg_minor.get(),
            self.avg_major.get(), self.avg_majorTick.get(), self.avg_markersz.get(),
            self.avg_xlabelsz.get(), self.avg_ylabelsz.get(), self.avg_fwidth.get(
            ), self.avg_fheight.get(), self.output_filename.get(),
            self.location, self.mname.get(), self.temp.get(), self.bwidth.get(), self.ie.get(),
            self.delta.get(), self.filelist, self.dpi.get(), self.parent, self.hd.get()
        )

    def SA(self):
        FELion_Sa(self.fname, self.location, self.dpi.get(), self.parent)

    def Power(self):
        FELion_Power(self.fname, self.location, self.dpi.get(), self.parent)

    def Baseline(self):
        baseline_correction(self.fname, self.location,
                            self.dpi.get(), self.parent)

    def LivePlot(self):
        livePlot(self.fname, self.location, self.dpi.get(), self.parent)


class Mass(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="sea green")

        self.parent = parent
        self.location = "/"
        self.fname = ""
        self.filelist = []
        self.mname, self.temp, self.bwidth, self.ie = None, None, None, None

        self.widget = FELion_widgets(self, cnt=controller)

        self.widget.labels('Mass Spectrum', 0, 0.05, bg="sea green",
                           font=LARGE_FONT, relwidth=1, relheight=0.05)

        pages = ('Back to Home', 'Norm and Avg', 'Powerfile', 'Plot')
        pages_name = (StartPage, Normline, Powerfile, Plot)

        x, y = 0.15, 0.9
        for name, pages_n in zip(pages, pages_name):
            self.widget.buttons(name, x, y, controller.show_frame, pages_n)
            x += 0.15

        self.widget.buttons('Browse', 0.1, 0.1,
                            controller.open_dir, self, mass_files_type)
        self.widget.labels('Mass File', 0.1, 0.24)

        self.location_label = self.widget.labels(
            self.location, 0.22, 0.14, bd=0, relwidth=0.7, relheight=0.06)
        self.fname_label = self.widget.labels(
            self.fname, 0.22, 0.24, bd=0, relwidth=0.15, relheight=0.06)

        controller.init_labels(self)

        # self.save = self.widget.entries('Check', 'Save', 0.4, 0.2, default = False)
        self.combine = self.widget.entries(
            'Check', 'Combine', 0.6, 0.2, default=False)

        self.widget.buttons('Select File(s)', 0.75, 0.2,
                            controller.openfilelist, self, mass_files_type)
        self.flist_label = self.widget.labels(
            'Filelists', 0.84, 0.7, bd=0, relwidth=0.15, relheight=0.2)

        self.avg_minor.set(1)
        self.avg_major.set(10)

        self.widget.buttons('Mass Spec', 0.7, 0.3, self.MassSpec_func)

    def MassSpec_func(self):
        massSpec(
            self.avg_title.get(), self.avg_ts.get(), self.avg_lgs.get(
            ), self.avg_minor.get(), self.avg_major.get(), self.avg_majorTick.get(),
            self.avg_xlabelsz.get(), self.avg_ylabelsz.get(), self.avg_fwidth.get(
            ), self.avg_fheight.get(), self.output_filename.get(),
            self.location, self.mname.get(), self.temp.get(), self.ie.get(),
            self.combine.get(), self.fname, self.filelist, self.dpi.get(), self.parent
        )


class Powerfile(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="sea green")
        self.location = "/"

        self.widget = FELion_widgets(self)

        self.widget.labels('Powerfile Generator', 0, 0.05, bg="sea green",
                           font=LARGE_FONT, relwidth=1, relheight=0.05)

        pages = ('Back to Home', 'Norm and Avg', 'Mass Spec', 'Plot')
        pages_name = (StartPage, Normline, Mass, Plot)

        x, y = 0.15, 0.9
        for name, pages_n in zip(pages, pages_name):
            self.widget.buttons(name, x, y, controller.show_frame, pages_n)
            x += 0.15

        self.date = datetime.datetime.now().strftime("%d_%m_%y-#")

        self.location_label = self.widget.labels(
            self.location, 0.22, 0.14, bd=0, relwidth=0.7, relheight=0.06)

        self.widget.buttons('Select Folder', 0.1, 0.1,
                            self.open_full_dir, 0.22, 0.14)
        self.widget.labels('Filename:', 0.1, 0.3)

        self.filename = self.widget.entries('Entry', self.date, 0.3, 0.3, bd=5)

        self.quote = """#POWER file\n# 10 Hz FELIX\n#\n#SHOTS=26\n#INTERP=linear\n#    IN_no_UM (if one deletes the "no" the firs number will be in \mu m\n# wavelength/cm-1      energy/pulse/mJ\n"""
        self.power = self.widget.entries('power_box', self.quote, 0.15, 0.4)

        self.widget.buttons('Save', 0.5, 0.3, self.save_powerfile)

    def open_full_dir(self, x, y):
        self.location = self.widget.open_full_dir()
        self.location_label.config(text=self.location)

    def save_powerfile(self):

        os.chdir(self.location)
        print(
            f'Filename: {self.filename.get()}.pow\nLocation: {self.location}\n')

        if isfile(f'./{self.filename.get()}.pow'):
            if messagebox.askokcancel('Overwrite?', f'File {self.filename.get()}.pow already exist.\nDo you want to overwrite?'):
                with open(f'./{self.filename.get()}.pow', 'w') as f:
                    f.write(self.power.get("1.0", "end-1c"))
                ShowInfo('Saved', f'File {self.filename.get()}.pow saved.')
                print(f'File {self.filename.get()}.pow saved.\n')
        else:
            with open(f'./{self.filename.get()}.pow', 'w') as f:
                f.write(self.power.get("1.0", "end-1c"))
            ShowInfo('Saved', f'File {self.filename.get()}.pow saved.')
            print(f'File {self.filename.get()}.pow saved.\n')


class Plot(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="sea green")

        self.parent = parent
        self.location = "/"
        self.fname = ""
        self.filelist = []
        self.full_name = ''

        self.widget = FELion_widgets(parent=self, cnt=controller)

        self.widget.labels('Plot', 0, 0.05, bg="sea green",
                           font=LARGE_FONT, relwidth=1, relheight=0.05)

        pages = ('Back to Home', 'Norm and Avg', 'Mass Spec', 'Powerfile')
        pages_name = (StartPage, Normline, Mass, Powerfile)

        x, y = 0.15, 0.9
        for name, pages_n in zip(pages, pages_name):
            self.widget.buttons(name, x, y, controller.show_frame, pages_n)
            x += 0.15

        self.widget.buttons('Browse', 0.1, 0.1,
                            controller.open_dir, self, all_files_type)
        self.widget.labels('Filename', 0.1, 0.24)

        self.location_label = self.widget.labels(
            self.location, 0.22, 0.14, bd=0, relwidth=0.7, relheight=0.06)
        self.fname_label = self.widget.labels(
            self.fname, 0.22, 0.24, bd=0, relwidth=0.15, relheight=0.06)

        self.combine = self.widget.entries(
            'Check', 'Combine', 0.22, 0.34, default=False)
        self.widget.buttons('Select File(s)', 0.1, 0.34,
                            controller.openfilelist, self, all_files_type)
        self.flist_label = self.widget.labels(
            'Filelists', 0.1, 0.55, bd=0, relwidth=0.15, relheight=0.2)

        self.widget.labels('DPI', 0.65, 0.23)
        self.dpi = self.widget.entries('Entry', 100, 0.75, 0.23, bd=5)

        self.widget.buttons('Timescan', 0.4, 0.3,
                            self.timescan_func, help='Plot timescan files')
        self.widget.buttons('kinetics', 0.52, 0.3, self.kinetics_func,
                            help='Simulate kinetics of the reaction from Timescan file')
        self.widget.buttons('Depletion', 0.65, 0.3, self.depletion_func,
                            help='Select two timescan files to see the depletion; and enter power_on, power_off and n')
        self.depletion_power = self.widget.entries('Entry',  'power_on, power_off, n_shots', 0.65,
                                                   0.4, bd=5, relwidth=0.25, help='Enter Power_ON, Power_OFF and N_Shots (comma separated)')

        self.widget.buttons('PowerPlot', 0.4, 0.4,
                            self.powerplot_func, help='For plotting .pow files')
        self.widget.buttons('JustPlot', 0.52, 0.4, self.just_plot_func,
                            help='Use it to plot any data file(s) with two columns')

        self.widget.buttons('Exp-Theory', 0.4, 0.55, self.avg_theory_func,
                            help='Plot exp and theoreitical data together')
        self.theory_scaling = self.widget.entries(
            'Entry', 0.97, 0.52, 0.58, bd=5, help='Scaling the theoretical values')
        self.smooth = self.widget.entries(
            'Entry', '21, 6', 0.52, 0.68, bd=5, help='Savitzky–Golay filter for smoothening data: Window_length, polyorder')

        self.show_original = self.widget.entries(
            'Check', 'Original', 0.4, 0.65, default=False, help='Compare smoothened data with original')

    def timescan_func(self):
        timescanplot(
            self.fname, self.location, self.dpi.get(), self.parent
        )

    def kinetics_func(self):
        kinetics(
            self.fname, self.location, self.dpi.get(), self.parent
        )

    def depletion_func(self):
        depletionPlot(
            self.filelist, self.location, self.depletion_power.get(), self.dpi.get(), self.parent
        )

    def powerplot_func(self):
        power_plot(
            self.fname, self.filelist, self.combine.get(),
            self.location, self.dpi.get(), self.parent
        )

    def just_plot_func(self):
        plot(
            self.fname, self.filelist, self.combine.get(
            ), self.location, self.dpi.get(), self.parent
        )

    def avg_theory_func(self):
        exp_theory(
            self.filelist, self.location, self.dpi.get(), self.show_original.get(
            ), self.theory_scaling.get(), self.smooth.get(), self.parent
        )

# Closing Program


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()


###################################################################################################################################################
app = FELion()
app.tk.call('tk', 'scaling', 4.0)

icons_locations = "C:/FELion-GUI/software/"
app.protocol("WM_DELETE_WINDOW", on_closing)

shutdown = PhotoImage(file=join(icons_locations, "power.png"))
restarticon = PhotoImage(file=join(icons_locations, "restart.png"))

power = ttk.Button(app, image=shutdown, text='power',
                   command=lambda: app.destroy())
restart = ttk.Button(app, image=restarticon, text='restart', command=lambda: os.execl(
    sys.executable, sys.executable, *sys.argv))

restart.place(relx=0.95, rely=0.05)
power.place(relx=0.95, rely=0.15)

app.mainloop()
###################################################################################################################################################
