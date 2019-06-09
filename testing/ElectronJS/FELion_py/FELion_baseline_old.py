#!/usr/bin/python3
import sys
import copy
import matplotlib
matplotlib.use('TkAgg')
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pylab as P
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.mlab import dist_point_to_segment

from scipy.interpolate import interp1d
import os
from os.path import dirname, isdir, isfile, join

import shutil
from tkinter import Tk, messagebox

from FELion_definitions import move, copy, ErrorInfo, ShowInfo

#These 2 values are used when guessing the baseline:
PPS = 5         #points around the value to average
NUM_POINTS = 10
baseline = None

########################################################################################

def ReadBase(basefile):
    #open file and skip sharps
    interpol='cubic'
    wl, cnt = [],[]
    with open(f'./DATA/{basefile}') as f:
        for line in f:
            if line[0] == '#':
                if line.find('INTERP')==1:
                    interpol = line.split('=')[-1].strip('\n')
                continue
            else:
                x, y, = line.split()
                wl.append(float(x))
                cnt.append(float(y))
    
    return np.array(wl), np.array(cnt), interpol

# Class for Baseline Calibration
class BaselineCalibrator(object):
    """
    Defines a baseline and is used to interpolate baseline for 
    any given wavenumber
    """
    def __init__(self, basefile, ms=None):

        self.ms = ms
        
        self.Bx, self.By, self.interpol = ReadBase(basefile)
        self.f = interp1d(self.Bx, self.By, kind=self.interpol)

    def val(self, x):
        return self.f(x)

    def plot(self, ax):

        x = np.arange(self.Bx.min(), self.Bx.max(), 0.5)
        ax.plot(x, self.val(x), marker='', ls='-', c='b')

        if self.ms is not None:
            ax.plot(self.Bx, self.By, marker='s', ls='', ms=self.ms, c='b', markeredgecolor='b', animated=True, label='Baseline')
        else:
            ax.plot(self.Bx, self.By, marker='s', ls='', ms=5, c='b', markeredgecolor='b', animated=True)
        
########################################################################################


class InteractivePoints(object):
    """
    Line editor
    Keys:
      'd' delete the vertex under point
      'a' insert a vertex at point
    """

    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, figure, ax, xs, ys, data, save, fname):
        self.ax = ax
        canvas = figure.canvas
        self.data = data
        self.save = save
        self.fname = fname
        self.figure = figure

        self.line = Line2D(xs, ys, marker='s', ls='', ms=6, c='b', markeredgecolor='b', animated=True)
        self.ax.add_line(self.line)
        
        #Interpolated Line:
        self.inter_xs = np.arange(xs[0], xs[-1])
        self.funcLine = Line2D([], [], marker='', ls='-', c='b', animated=True)
        self.ax.add_line(self.funcLine)
        self.redraw_f_line()

        self._ind = None  # the active vert

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('key_press_event', self.key_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas

    def redraw_f_line(self):
        Bx, By = self.line.get_data()
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

    def key_press_callback(self, event):
        'whenever a key is pressed'
        #global data, baseline
        if not event.inaxes:
            return
        elif event.key == 'w':
            ind = self.get_ind_under_point(event)
            if ind is not None:
                xy = np.asarray(self.line.get_data())
                #makes average of few points around the cursor
                i = self.data[0].searchsorted(event.xdata)
                if i + PPS > self.data[0].size:
                    i = self.data[0].size - PPS
                xy[1][ind] = self.data[1][i:i+PPS].mean()
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
            baseline = self.line.get_data()

            print(f'New Baseline: {baseline}')
            if self.save:
                SaveBase(self.fname, baseline)
                if isfile(join(os.getcwd(), 'DATA', f'{self.fname}.base')):
                    print(f'{self.fname}.base is SAVED')
                    ShowInfo('SAVED', f'{self.fname}.base file is saved in /DATA directory')
                    #plt.close(self.figure)
            #plt.close('all')
        
        self.redraw_f_line()
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
################################################################################
'''
def felix_read_file(fname):
    """
    Reads data from felix meassurement file
    Input: filename
    Output: data[0,1]   0 - wavenumber, 1 - intensity
    """
    
    sa_factor = 1.0
    #open file and skip sharps
    wl, cnt, sa = [],[],[]
    f = open('DATA/' + fname + '.felix')
    for line in f:
        if line[0] == '#':
            if line.find("3HARM")==1:
                sa_factor=2.0
            continue
        else:
            if len(line.split()) < 4: continue;
            x, y, z, q, *rest = line.split()
            wl.append(float(x))
            cnt.append(float(z))
            sa.append(float(q)*sa_factor)
    
    f.close()
    data = np.array([wl, cnt, sa])

    indices = data[0].argsort()
    wl_min_f = data[0][indices[0]]
    wl_max_f = data[0][indices[-1]]
    print("--------------------------------------------------------------------------------")
    print('FILE: ', fname, '\tWavelength in file:' , wl_min_f, '-', wl_max_f, 'PONTS: ', len(data[0][:]))
    
    res = np.take(data, indices, 1)
    return res'''

def felix_read_file(felixfile):

    file = np.genfromtxt(f'./DATA/{felixfile}')
    if felixfile.endswith('.felix'): data = file[:,0], file[:,2], file[:, 3]
    elif felixfile.endswith('.cfelix'): data = file[:,0], file[:,1], file[:, 2]
    else: return ErrorInfo('FELIX FILE', 'Please select a .felix or .cfelix file')
    return np.take(data, data[0].argsort(), 1)

def GuessBaseLine(data):
    """
    Guesses the baseline according to real points in the datafile.
    makes NUM_POINTS baseline defining points 
    """
    max_n = len(data[0]) - PPS
    Bx, By = [data[0][0]-0.1], [data[1][0]]             #NOTE teh 0.1 is here to be 
    #sure all the frequencies are in baseline calib. range
    for i in range(0, max_n, int(max_n/NUM_POINTS)):
        x = data[0][i:i+PPS].mean()
        y = data[1][i:i+PPS].mean()
        Bx.append(x)
        By.append(y)
    Bx.append(data[0][-1]+0.1)
    By.append(data[1][-1])

    return np.array(Bx), np.array(By)

def SaveBase(fname, baseline):
    b = np.asarray(baseline)
    f = open('DATA/' + fname + '.base','w')
    f.write("#Baseline generated for " + fname + ".felix data file!\n")
    f.write("#BTYPE=cubic\n")
    for i in range(len(b[0])):
        f.write("{:8.3f}\t{:8.2f}\n".format(b[0][i], b[1][i]))

def main(fname=""):
    if fname == "":
        fname = input("Please enter the file name (without .felix): ")
    if(fname.find('felix')):
        fname = fname.split('.')[0]
    
    my_path = os.getcwd()

    if os.path.isdir('EXPORT'):
        print("EXPORT folder exist")
    else:
        os.mkdir('EXPORT')
        print("EXPORT folder created.")
        
    if os.path.isdir('OUT'):
        print("OUT folder exist")
    else:
        os.mkdir('OUT')
        print("OUT folder created.")

    if os.path.isdir('DATA'):
        print("DATA folder exist")
    else:
        os.mkdir('DATA')
        print("DATA folder created.")

    filename = fname + ".felix"

    if os.path.isfile(filename):
        print("File exist, Copying to the DATA folder to process.")
        shutil.copyfile(my_path + "/{}".format(filename), my_path + "/DATA/{}".format(filename))

    data = felix_read_file(fname)

    #Check wether the baslien file exists
    if not os.path.isfile('DATA/'+fname+'.base'):
        print("Guessing baseline from .felix file!")
        xs, ys = GuessBaseLine(data)
    else:
        print("Reading baseline from .base file!")
        xs, ys, *rest = ReadBase(fname)

    fig, ax = plt.subplots()

    p = InteractivePoints(fig, ax, xs, ys)
    ax.plot(data[0], data[1], ls='', marker='o', ms=5, markeredgecolor='r', c='r')

    print("\nUSAGE:\nBlue baseline points are dragable...\
           \nKeys:\n\
    'a' - adds a point at current cursor position\n\
    'd' - delets a point at current cursor position\n\
    'w' - moves the point to the 'average' value at given x position\n\
    'q' - stores baseline in .base file and quits!\n")

    ax.set_title('BASELINE points are drag-able!')
    ax.set_xlim((data[0][0]-70, data[0][-1]+70))
    ax.set_xlabel("wavenumber (cm-1)")
    ax.set_ylabel("Counts")
    plt.show()
    
    #Powerfile check
    powerfile = fname + ".pow"
    if not os.path.isfile(powerfile):
        print("NOTE: You don't have .pow file so you can't plot the data yet but you can make the baseline.")
    elif os.path.isfile(powerfile):
        shutil.copyfile(my_path + "/{}".format(powerfile), my_path + "/DATA/{}".format(powerfile))
        print("Powerfile is copied to the DATA folder")

    if baseline != None:
        SaveBase(fname, baseline)
    return

def baseline_correction(fname, location, save):

    try:
        
        folders = ["DATA", "EXPORT", "OUT"]
        back_dir = dirname(location)
        
        if set(folders).issubset(os.listdir(back_dir)): 
            os.chdir(back_dir)
            my_path = os.getcwd()
        
        else: 
            os.chdir(location)
            my_path = os.getcwd()
            
        if(fname.find('felix')>=0):
            fname = fname.split('.')[0]

        filename = fname + ".felix"
        basefile = fname + ".base"
        powerfile = fname + ".pow"
        files = [filename, powerfile, basefile]

        for dirs, filenames in zip(folders, files):
            if not isdir(dirs): os.mkdir(dirs)
            if isfile(filenames): move(my_path, filenames)

        data = felix_read_file(fname)

        #Check wether the baslien file exists
        if not os.path.isfile('DATA/'+fname+'.base'):
            print("Guessing baseline from .felix file!")
            xs, ys = GuessBaseLine(data)
        else:
            print("Reading baseline from .base file!")
            xs, ys, *rest = ReadBase(fname)
        
        #ShowInfo('Info', "NOTE: Press 'X' to save the baseline\nThen Close the plot Manually")

        fig, ax = plt.subplots()

        p = InteractivePoints(fig, ax, xs, ys, data, save, fname)
        ax.plot(data[0], data[1], ls='', marker='o', ms=5, markeredgecolor='r', c='r')

        print("\nUSAGE:\nBlue baseline points are dragable...\
            \nKeys:\n\
        'a' - adds a point at current cursor position\n\
        'd' - delets a point at current cursor position\n\
        'w' - moves the point to the 'average' value at given x position\n\
        'x' - stores baseline in .base file and quits!\n")

        ax.set_title('BASELINE points are drag-able!')
        ax.set_xlim((data[0][0]-70, data[0][-1]+70))
        ax.set_xlabel("wavenumber (cm-1)")
        ax.set_ylabel("Counts")
        plt.show()
        #plt.close('all')
        
    except Exception as e:
        ErrorInfo("ERROR: ", e)

if __name__ == "__main__":
    main()