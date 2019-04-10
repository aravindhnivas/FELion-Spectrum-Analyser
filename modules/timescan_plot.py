#!/usr/bin/python3

# Built-In modules
import os
from time import time as check_time

# DATA analysis modules
import numpy as np
from uncertainties import unumpy as unp

# FELion Modules
from FELion_definitions import ErrorInfo, FELion_Toplevel, get_iterations, get_skip_line, var_find

# Tkinter modules
from tkinter import Toplevel, ttk, BooleanVar

####################################### Modules Imported #######################################

def timescanplot(scanfile, location, dpi, parent, depletion = False):

    t0 = check_time()
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
    data_dict = {}
    for num, iteration in enumerate(iterations):
        
        k = iteration*cycle
        
        print(f'### START {num} ###\n')
        print(f'DATA collecting: data[:, 2][{j}:{k+j}]\n')
        
        mass_value = data[:, 0][j:k+j][0]
        mass_sort = data[:, 2][j:k+j].reshape(iteration, cycle).mean(axis = 0)
        error_sort = data[:, 2][j:k+j].reshape(iteration, cycle).std(axis = 0)
        
        mass = np.append(mass, mass_value)
        mean = np.append(mean, mass_sort)
        error = np.append(error, error_sort)

        # Saving it in dictionary
        data_dict[f'{mass_value}'] = mass_sort
        data_dict[f'{mass_value}_error'] = error_sort
        
        j = k + j
        
        print(f'Mass {num} is {mass_value} with counts: {mass_sort}\t{mass_sort.shape}\n')
        print(f'Error {num} for {mass_value}: {error_sort}\t{error_sort.shape}\n')
        print(f'Before\nMean: {mean.shape}\t Error: {error.shape}\n')
        print(f'Total Mass collected: {mass}\n')
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
    title_name = f'Timescan: {scanfile}'
    root = Toplevel(parent)

    tk_widget = FELion_Toplevel(root, title_name, location)

    fig, canvas = tk_widget.figure(dpi, figsize=(15,5))
    ax = fig.add_subplot(111)
    
    frame = tk_widget.get_widget_frame()

    log = BooleanVar()
    log_btn = ttk.Checkbutton(frame, text = 'Log', variable = log)
    log_btn.place(relx = 0.1, rely =  0.3, relwidth = 0.5, relheight = 0.05)
    log.set(False)

    ####################################### PLOTTING DETAILS #######################################

    check_text = mass.astype(str)
    tk_widget.check_button_maker(check_text)

    ax.errorbar(time, unp.nominal_values(sum_mean_with_error), unp.std_devs(sum_mean_with_error), fmt = '--', label = f'SUM TOTAL', color = 'k')
    
    axes = {}
    for n, i in enumerate(check_text):
        lg = f'{mass[n]}[{iterations[n]}]; B0: {t_b0}ms; Res: {t_res}'
        axes[i] = ax.errorbar(time, mean[n], error[n], fmt='.-', label = lg)
    
    # figure details      
    ax.set_title('Time Scan plot for %s'%scanfile)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Counts')
    ax.legend()
    ax.grid(True)

    def update():
        t0 = check_time()

        ax.clear()
        ax.errorbar(time, unp.nominal_values(sum_mean_with_error), unp.std_devs(sum_mean_with_error), fmt = '--', label = f'SUM TOTAL', color = 'k')
        check_dict = tk_widget.get_check_values()
        for n, i in enumerate(check_text):
            if check_dict[f'{i}_value'].get():
                lg = f'{mass[n]}[{iterations[n]}]; B0: {t_b0}ms; Res: {t_res}'
                ax.errorbar(time, mean[n], error[n], fmt='.-', label = lg)
        
        ax.set_title('Time Scan plot for %s'%scanfile)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Counts')
        ax.legend()
        ax.grid(True)

        t0 = check_time()

        if log.get(): 
            ax.set_yscale('log')
        else: 
            ax.set_yscale('linear')
            ax.ticklabel_format(style='sci', axis='y', scilimits = (0, 0))

        canvas.draw()

        t1 = check_time()

        print(f'Redrawn in {(t1-t0)*100:.2f} ms')

    update_btn = ttk.Button(frame, text = 'Update Plot', command = lambda: update())
    update_btn.place(relx = 0.2, rely =  0.6, relwidth = 0.5, relheight = 0.05)
    

    ####################################### END Plotting details #######################################
    canvas.draw() # drawing in the tkinter canvas: canvas drawing board
    ####################################### END Tkinter figure #######################################
    t1 = check_time()

    time_log = (t1-t0)*100
    print(f'Timescan plot completed in {time_log:.2f} ms\n')



