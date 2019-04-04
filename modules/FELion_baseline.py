#!/usr/bin/python3

# FELion Module
from FELion_definitions import move, FELion_Toplevel, ShowInfo
from FELion_power import PowerCalibrator
from FELion_sa import SpectrumAnalyserCalibrator

# Built-In Module
import os
from os.path import dirname, isdir, isfile, join

# DATA analysis modules
from scipy.interpolate import interp1d
import numpy as np

# Tkinter Modules
from tkinter import Toplevel, ttk, Frame, Entry, StringVar
from tkinter.messagebox import askokcancel

# Matplotlib modules
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec as grid

# Matplotlib Modules for tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

###################################################################################################

class Create_Baseline():

    epsilon = 5

    def __init__(self, felixfile, location, dpi, parent):

        self.parent = parent
        self.dpi = dpi

        self.felixfile = felixfile
        self.fname = felixfile.split('.')[0]
        self.basefile = f'{self.fname}.base'
        self.powerfile = f'{self.fname}.pow'

        self.baseline = None
        self.data = None
        
        back_dir = dirname(location)
        folders = ["DATA", "EXPORT", "OUT"]
        if set(folders).issubset(os.listdir(back_dir)): 
            self.location = back_dir
        else: 
            self.location = location
   
        os.chdir(self.location)
        for dirs in folders: 
            if not isdir(dirs): os.mkdir(dirs)
            if isfile(self.felixfile): move(self.location, self.felixfile)
            if isfile(self.basefile): move(self.location, self.basefile)
            if isfile(self.powerfile): move(self.location, self.powerfile)

    def felix_read_file(self):

        file = np.genfromtxt(f'DATA/{self.felixfile}')
        wn, count, sa = file[:,0], file[:,2], file[:,3]
        data = wn, count, sa
        data = np.take(data, data[0].argsort(), 1)
        self.data = data
    
    def ReadBase(self):

        file = np.genfromtxt(f'DATA/{self.basefile}')
        self.xs, self.ys = file[:,0], file[:,1]
        with open(f'DATA/{self.basefile}', 'r') as f:
            self.interpol = f.readlines()[1].strip().split('=')[-1]
    
    def SaveBase(self):
        self.baseline = self.line.get_data()
        b = np.asarray(self.baseline)
        with open(f'DATA/{self.basefile}', 'w') as f:
            f.write(f'#Baseline generated for {self.fname}.felix data file!\n')
            f.write("#BTYPE=cubic\n")
            for i in range(len(b[0])):
                f.write("{:8.3f}\t{:8.2f}\n".format(b[0][i], b[1][i]))
        
        if isfile(f'DATA/{self.basefile}'):
            print(f'{self.basefile} is SAVED')
            ShowInfo('SAVED', f'{self.basefile} file is saved in /DATA directory')
    
    def GuessBaseLine(self, PPS, NUM_POINTS):
        max_n = len(self.data[0]) - PPS
        Bx, By = [self.data[0][0]-0.1], [self.data[1][0]]

        for i in range(0, max_n, int(max_n/NUM_POINTS)):
            x = self.data[0][i:i+PPS].mean()
            y = self.data[1][i:i+PPS].mean()
            Bx.append(x)
            By.append(y)
        Bx.append(self.data[0][-1]+0.1)
        By.append(self.data[1][-1])

        self.xs, self.ys = Bx, By
        self.PPS = PPS

    def InteractivePlots(self, start = True):
        if start: 
            self.tkbase()
            self.startplot(self.ax, start)
        
        else:
            self.startplot(self.ax0, start)

    def startplot(self, ax, start = True):
        self.normline_data_set = not start
        self.ax = ax
        
        self.line = Line2D(self.xs, self.ys, marker='s', ls='', ms=6, c='b', markeredgecolor='b', animated=True)
        self.ax.add_line(self.line)        
        
        self.inter_xs = np.arange(self.xs[0], self.xs[-1])
        self.funcLine = Line2D([], [], marker='', ls='-', c='b', animated=True)
        self.ax.add_line(self.funcLine)

        self.redraw_f_line()
        self._ind = None

        self.canvas.mpl_connect('draw_event', self.draw_callback)
        self.canvas.mpl_connect('button_press_event', self.button_press_callback)
        self.canvas.mpl_connect('key_press_event', self.key_press_callback)
        self.canvas.mpl_connect('button_release_event', self.button_release_callback)
        self.canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
    
    def redraw_f_line(self):
        Bx, By = np.array(self.line.get_data())
        self.inter_xs = np.arange(Bx.min(), Bx.max())

        f = interp1d(Bx, By, kind='cubic')
        self.funcLine.set_data((self.inter_xs, f(self.inter_xs)))

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.line)
        self.ax.draw_artist(self.funcLine)
        self.canvas.blit(self.ax.bbox)

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'

        xy = np.asarray(self.line.get_data()).T
        xyt = self.line.get_transform().transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if event.button != 1:
            return
        self._ind = None

        if self.normline_data_set:
            self.redraw_normline()

    def redraw_normline(self):
        new_f = interp1d(*self.line.get_data(), kind = 'cubic')
        new_intensity = -np.log(self.data[1]/new_f(self.data[0])) / self.powCal.power(self.data[0]) / self.powCal.shots(self.data[0]) *1000
        self.normline_data.set_ydata(new_intensity)
        self.ax1.set_ylim(ymax = new_intensity.max()+1)
        self.canvas.draw()
    
    def motion_notify_callback(self, event):
        'on mouse movement'
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        xy = np.asarray(self.line.get_data())
        xy[0][self._ind], xy[1][self._ind] = x, y
        self.line.set_data((xy[0], xy[1]))

        self.redraw_f_line()

        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.line)
        self.ax.draw_artist(self.funcLine)
        self.canvas.blit(self.ax.bbox)

    def key_press_callback(self, event):
        'whenever a key is pressed'
        key_press_handler(event, self.canvas, self.toolbar)
        if not event.inaxes:
            return
        elif event.key == 'w':
            ind = self.get_ind_under_point(event)
            if ind is not None:
                xy = np.asarray(self.line.get_data())
                #makes average of few points around the cursor
                i = self.data[0].searchsorted(event.xdata)
                if i + self.PPS > self.data[0].size:
                    i = self.data[0].size - self.PPS
                xy[1][ind] = self.data[1][i:i+self.PPS].mean()
                self.line.set_data((xy[0], xy[1]))
        elif event.key == 'd':
            ind = self.get_ind_under_point(event)
            if ind is not None:
                xy = np.asarray(self.line.get_data()).T
                xy = np.array([tup for i, tup in enumerate(xy) if i != ind])
                self.line.set_data((xy[:,0], xy[:,1]))
        elif event.key == 'a':
            xy = np.asarray(self.line.get_data())
            xy = np.append(xy,[[event.xdata], [event.ydata]], axis=1)
            self.line.set_data((xy[0], xy[1]))
        
        elif event.key == 'x':
            ind = self.get_ind_under_point(event)
            print(f'Datas: {event.xdata}, {event.ydata}')
            new_data = self.data[1]
            print(new_data, self.data[1])
            print(np.argwhere((new_data >= event.ydata - 10) & (new_data <= event.ydata + 10)))
            
        
        if self.normline_data_set:
            self.redraw_normline()

        self.redraw_f_line()
        self.canvas.draw()

    def tkbase(self, get = False, start = True):

        self.root = Toplevel(master = self.parent)
        self.root.wm_title('Baseline Correction')
        self.root.wm_geometry('1000x600')

        self.canvas_frame = Frame(self.root, bg = 'white')
        self.canvas_frame.place(relx = 0, rely = 0, relwidth = 0.8, relheight = 1)

        self.widget_frame = Frame(self.root, bg = 'light grey')
        self.widget_frame.place(relx = 0.8, rely = 0, relwidth = 0.2, relheight = 1)

        self.name = StringVar()
        self.filename = Entry(self.widget_frame, textvariable = self.name, font = ("Verdana", 10, "italic"), bd = 5)
        self.name.set('plot')
        self.filename.place(relx = 0.1, rely = 0.1, relwidth = 0.5, relheight = 0.05)

        self.button = ttk.Button(self.widget_frame, text = 'Save', command = lambda: self.save_tkbase(start))
        self.button.place(relx = 0.1, rely = 0.2, relwidth = 0.5, relheight = 0.05)

        if get: return self.root, self.canvas_frame, self.widget_frame

        self.figure_tkbase()

    def figure_tkbase(self, get = False, get_figure = False):
        
        self.fig = Figure(dpi = self.dpi)

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.canvas_frame)
        self.canvas.get_tk_widget().place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

        if get_figure: return self.fig, self.canvas

        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(top = 0.95, bottom = 0.2, left = 0.1, right = 0.9)
        self.ax.plot(self.data[0], self.data[1], ls='', marker='o', ms=5, markeredgecolor='r', c='r')

        self.ax.set_title('BASELINE points are drag-able!')
        self.ax.set_xlim((self.data[0][0]-70, self.data[0][-1]+70))
        self.ax.set_xlabel("wavenumber (cm-1)")
        self.ax.set_ylabel("Counts")

        if get: return self.fig, self.ax, self.canvas
        
        self.canvas.draw()

    def save_tkbase(self, start):
        if start:
            self.SaveBase()
            
            if isfile(f'{self.name.get()}.png'): 
                    if askokcancel('Overwrite?', f'File: {self.name.get()}.png already present. \nDo you want to Overwrite the file?'): 
                            self.fig.savefig(f'OUT/{self.name.get()}.png')
                            ShowInfo('SAVED', f'File: {self.name.get()}.png saved in \n{self.location}/OUT directory')
            else: 
                    self.fig.savefig(f'OUT/{self.name.get()}.png')
                    ShowInfo('SAVED', f'File: {self.name.get()}.png saved in \n{self.location}/OUT\n directory')
        else:
            self.export_file()
            if isfile(f'EXPORT/{self.fname}.dat'): ShowInfo('SAVED', f'File: {self.fname}.dat saved in /EXPORT directory')
            self.fig.savefig(f'OUT/{self.name.get()}.png')
            if isfile(f'OUT/{self.name.get()}.png'): ShowInfo('SAVED', f'File: {self.name.get()}.png saved in /OUT directory')

    def plot(self):
        print(f'\nLocation: {self.location}\nFilename: {self.felixfile}')
        
        self.felix_read_file()

        if isfile(f'DATA/{self.basefile}'): self.ReadBase() # Read baseline file if exist else guess it
        else: self.GuessBaseLine(PPS = 5, NUM_POINTS = 10)

        self.InteractivePlots()
    
    def get_plot_details(self):
        return self.figure_tkbase(get = True)
    
    def get_figure_details(self):
        return self.figure_tkbase(get_figure = True)
    
    def get_tkinter_details(self):
        return self.tkbase(get=True)

    def livePlot(self):

        self.root, self.canvas_frame, self.widget_frame = self.tkbase(get = True, start = False)
        self.fig, self.canvas = self.figure_tkbase(get_figure = True)

        spec = grid(ncols=2, nrows=1, figure=self.fig)

        self.ax0 = self.fig.add_subplot(spec[0, 0])
        self.ax1 = self.fig.add_subplot(spec[0, 1])

        self.InteractivePlots(start = False)

        self.powCal = PowerCalibrator(self.fname)
        self.saCal = SpectrumAnalyserCalibrator(self.fname)
        self.wavelength = self.saCal.sa_cm(self.data[0])
        self.f = interp1d(*self.line.get_data(), kind = 'cubic')
        self.intensity = -np.log(self.data[1]/self.f(self.data[0])) / self.powCal.power(self.data[0]) / self.powCal.shots(self.data[0]) *1000 

        self.normline_data, = self.ax1.plot(self.wavelength, self.intensity, ls='-', marker='o', ms=2, c='r', markeredgecolor='k', markerfacecolor='k')

        self.ax0.plot(self.data[0], self.data[1], ls='', marker='o', ms=5, markeredgecolor='r', c='r')

        self.fig.suptitle('Interactive Plot')
        self.ax0.set_title('Baseline Correction')
        self.ax0.set_xlim((self.data[0][0]-70, self.data[0][-1]+70))
        self.ax0.set_xlabel("Wavenumber (cm-1)")
        self.ax0.set_ylabel("Counts")
        self.canvas.draw()
        
        self.ax1.set_title('Normalised Intensity')
        self.ax1.set_xlabel('Wavenumber (Calibrated)')
        self.ax1.set_ylabel('Intensity (Normalised)')
        self.ax1.grid(True)
        self.ax0.grid(True)

    def export_file(self):
        self.SaveBase()
        with open(f'EXPORT/{self.fname}.dat', 'w') as f:
            f.write("#DATA points as shown in lower figure of: " + self.fname + ".pdf file!\n")
            f.write("#wn (cm-1)       intensity\n")
            for i in range(len(self.wavelength)):
                f.write("{:8.3f}\t{:8.2f}\n".format(self.wavelength[i], self.intensity[i]))

        print(f'File {self.fname}.dat saved in EXPORT/ Directory')

def baseline_correction(felixfile, location, dpi, parent):
    
    base = Create_Baseline(felixfile, location, dpi, parent)

    print(f'\nLocation: {base.location}\nFilename: {base.felixfile}')

    base.felix_read_file() # read felix file
    if isfile(f'DATA/{base.basefile}'): base.ReadBase() # Read baseline file if exist else guess it
    else: base.GuessBaseLine(PPS = 5, NUM_POINTS = 10)

    base.InteractivePlots() # Plot

def livePlot(felixfile, location, dpi, parent):

    live = Create_Baseline(felixfile, location, dpi, parent)

    print(f'\nLocation: {live.location}\nFilename: {live.felixfile}')
    live.felix_read_file() # read felix file
    if isfile(f'DATA/{live.basefile}'): live.ReadBase() # Read baseline file if exist else guess it
    else: live.GuessBaseLine(PPS = 5, NUM_POINTS = 10)
    
    live.livePlot()