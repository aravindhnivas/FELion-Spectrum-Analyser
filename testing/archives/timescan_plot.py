#!/usr/bin/python3

# Importing Modules

# Built-In modules
import os

# DATA analysis modules
from numpy import array, genfromtxt

# FELion Modules
from FELion_definitions import ErrorInfo, FELion_Toplevel

# Tkinter modules
from tkinter import Toplevel

####################################### Modules Imported #######################################

def timescanplot(fname, location, dpi, parent, depletion = False):
    try:
        ####################################### Initialisation #######################################

        os.chdir(location)

        var = {'res':'m03_ao13_reso', 'b0':'m03_ao09_width'}
        print(var)

        with open(fname, 'r') as f:
            f = array(f.readlines())
        for i in f:
            if not len(i.strip())==0 and i.split()[0]=='#':
                for j in var:
                    if var[j] in i.split():
                        var[j] = float(i.split()[-3])

        t_res, t_b0 = round(var['res']), int(var['b0']/1000)
        print(var)

        with open(fname, 'r') as f: file = f.readlines()
        
        skip = [num for num, line in enumerate(file) if 'ALL:' in line.split()]
        iterations = array([int(i.split()[-1]) for i in file if not len(i.strip())==0 and i.split()[0].startswith('#mass')])
        length = len(iterations)

        data = genfromtxt(fname, skip_header = skip[0]+1)

        cycle = int(len(data)/iterations.sum())
        time = data[:,1][:cycle]

        temp, temp1, temp2, mass, counts = [], [], [], [], []
        k = 0
        for i in range(len(iterations)):
            j = iterations[i]*cycle
            mass.append(data[:,0][k])
            counts.append(data[:,2][k:k+j])
            k += j
            
            for c in range(cycle):
                for l in range(iterations[i]):
                    temp.append(counts[i][(l*cycle)+c])
                temp1.append(temp)
                temp = []
            temp2.append(temp1)
            temp1 = []
            
        mean = [[array(temp2[i][j]).mean() for j in range(cycle)]for i in range(length)]
        error = [[(array(temp2[i][j]).std()) for j in range(cycle)]for i in range(length)]
        mass, mean, error = array(mass), array(mean), array(error)

        if depletion: 
            return mass, iterations, t_res, t_b0,  mean, error, time
            print('\nReturning from Timescan function\n')
        
        ####################################### END Initialisation #######################################

        ####################################### Tkinter figure #######################################

        ## Embedding figure to tkinter Toplevel
        title_name = 'Timescan'
        root = Toplevel(parent)
        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi, figsize=(15,5))
        ax = fig.add_subplot(111)

        ####################################### PLOTTING DETAILS #######################################

        for i in range(length):
            lg = "%.2f:[%i]; B0: %i ms, Res: %i"%(mass[i], iterations[i], t_b0, t_res)
            ax.errorbar(time, mean[i],error[i],fmt='.-', label = lg)
            
        ax.set_title('Time Scan plot for %s'%fname)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Counts')
        ax.legend()
        ax.grid(True)

        ####################################### END Plotting details #######################################

        canvas.draw() # drawing in the tkinter canvas: canvas drawing board
        
        ####################################### END Tkinter figure #######################################
   
    except Exception as e:
        ErrorInfo("ERROR", e)