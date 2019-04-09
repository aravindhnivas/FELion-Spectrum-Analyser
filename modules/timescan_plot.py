#!/usr/bin/python3

# Built-In modules
import os

# DATA analysis modules
import numpy as np
from uncertainties import unumpy as unp

# FELion Modules
from FELion_definitions import ErrorInfo, FELion_Toplevel, get_iterations, get_skip_line, var_find

# Tkinter modules
from tkinter import Toplevel

####################################### Modules Imported #######################################

def timescanplot(scanfile, location, dpi, parent, depletion = False):

    ####################################### Initialisation #######################################
    os.chdir(location)

    # Getting skip_line to reach the data points
    # Getting iterations of each mass timescan
    skip = get_skip_line(scanfile, location)
    iterations = get_iterations(scanfile, location)

    # opening File
    data = np.genfromtxt(scanfile, skip_header = skip)
    print(f'File shape: {data.shape}\n')

    # Calculating the time step cycle and total no of masses (run)
    cycle = int(len(data)/iterations.sum())
    run = len(iterations)

    # Time
    time = data[:, 1][: cycle]
    print(f'Time: {time}\t{time.shape}\n')

    # Calculating mean and std_devs
    j = 0
    mean, error = [], []
    mass = []
    for num, iteration in enumerate(iterations):
        
        k = iteration*cycle
        
        print(f'### START {num} ###\n')
        print(f'Before: data[:, 2][{j}:{k+j}]\n')
        
        mass_value = data[:, 0][j: k+j][0]
        mass_sort = data[:, 2][j:k+j].reshape(iteration, cycle).mean(axis = 0)
        error_sort = data[:, 2][j:k+j].reshape(iteration, cycle).std(axis = 0)
        
        mass = np.append(mass, mass_value)
        mean = np.append(mean, mass_sort)
        error = np.append(error, error_sort)
        
        j = k + j
        
        print(f'After: j: {j}\n')
        print(f'Mass {num}: {mass_sort}\t{mass_sort.shape}\n')
        print(f'Error {num}: {error_sort}\t{error_sort.shape}\n')
        print(f'Before\nMean: {mean.shape}\t Error: {error.shape}\n')
        print(f'Total Mass: {mass}\n')
        print(f'### END {num} ###\n\n')

    mean = mean.reshape(run, cycle)
    error = error.reshape(run, cycle)

    print(f'After\nMean: {mean.shape}\t Error: {error.shape}\n')

    # calculating the SUM
    mean_with_error = unp.uarray(mean, error)
    sum_mean_with_error = mean_with_error.sum(axis = 0)
    print(f'Mean with error: {mean_with_error.shape}\nSum with error: {sum_mean_with_error.shape}')
    
    # Getting B0 width and Mass resolution from Timescan file
    t_res, t_b0 = var_find(scanfile, location, time = True)

    if depletion: 
        print('\nReturning from Timescan function\n')
        return mass, iterations, t_res, t_b0,  mean, error, time

    ####################################### END Initialisation #######################################

    ####################################### Tkinter figure #######################################

    ## Embedding figure to tkinter Toplevel
    title_name = 'Timescan'
    root = Toplevel(parent)
    tk_widget = FELion_Toplevel(root, title_name, location)

    fig, canvas = tk_widget.figure(dpi, figsize=(15,5))
    ax = fig.add_subplot(111)

    ####################################### PLOTTING DETAILS #######################################

    ax.errorbar(time, unp.nominal_values(sum_mean_with_error), unp.std_devs(sum_mean_with_error), fmt = '--', label = f'SUM TOTAL')
    for i in range(run):
        lg = "%.2f:[%i]; B0: %i ms, Res: %i"%(mass[i], iterations[i], t_b0, t_res)
        ax.errorbar(time, mean[i], error[i], fmt='.-', label = lg)
        
    ax.set_title('Time Scan plot for %s'%scanfile)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Counts')
    ax.legend()
    ax.grid(True)

    ####################################### END Plotting details #######################################
    canvas.draw() # drawing in the tkinter canvas: canvas drawing board
    ####################################### END Tkinter figure #######################################