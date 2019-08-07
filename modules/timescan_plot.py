#!/usr/bin/python3

# Built-In modules
import os
from time import time as check_time
import itertools as it

# DATA analysis modules
import numpy as np
from uncertainties import unumpy as unp

# FELion Modules
from FELion_definitions import ErrorInfo, FELion_Toplevel, get_iterations, get_skip_line, var_find

# Tkinter modules
from tkinter import Toplevel, ttk, BooleanVar

# Error traceback
import traceback

####################################### Modules Imported #######################################

def timescanplot(scanfile, location, dpi, parent, **kw):

    try:

        if 'depletion' in kw:
            depletion = kw['depletion']
        else:
            depletion = False

        if 'kinetics' in kw:
            kinetics = kw['kinetics']
        else:
            kinetics = False

        t0 = check_time()

        ####################################### Initialisation #######################################
        os.chdir(location)

        skip = get_skip_line(scanfile, location)
        iterations = get_iterations(scanfile, location)

        # opening File
        data = np.genfromtxt(scanfile, skip_header=skip)
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
        m = {}

        mass_count = 0
        for num, iteration in enumerate(iterations):

            k = iteration*cycle

            print(f'### START {num} ###\n')
            print(f'DATA collecting: data[:, 2][{j}:{k+j}]\n')

            mass_value = data[:, 0][j:k+j][0]

            if mass_value in mass:
                mass_count += 1
                mass_value = f'{mass_value}_{mass_count}'

            mass_sort = data[:, 2][j:k +
                                   j].reshape(iteration, cycle).mean(axis=0)
            error_sort = data[:, 2][j:k +
                                    j].reshape(iteration, cycle).std(axis=0)

            mass = np.append(mass, mass_value)
            mean = np.append(mean, mass_sort)
            error = np.append(error, error_sort)

            m[f'{mass_value}'] = mass_sort
            m[f'e{mass_value}'] = error_sort

            j = k + j

            print(
                f'Mass {num} is {mass_value} with counts: {mass_sort}\t{mass_sort.shape}\n')
            print(
                f'Error {num} for {mass_value}: {error_sort}\t{error_sort.shape}\n')
            print(f'Before\nMean: {mean.shape}\t Error: {error.shape}\n')
            print(f'Total Mass collected: {mass}\n')
            print(f'### END {num} ###\n\n')

        mean = mean.reshape(run, cycle)
        error = error.reshape(run, cycle)

        print(f'After\nMean: {mean.shape}\t Error: {error.shape}\n')

        # Getting B0 width and Mass resolution from Timescan file
        t_res, t_b0 = var_find(scanfile, location, time=True)

        masslist = mass.astype(str)

        if depletion:
            print('\nDepeltion Measurements\n')
            return mass, iterations, t_res, t_b0,  mean, error, time

        if kinetics:
            print('\nKinetics Measurements\n')
            return time, m, masslist, iterations, t_res, t_b0

        ####################################### END Initialisation #######################################

        ####################################### Tkinter figure #######################################

        # Embedding figure to tkinter Toplevel
        title_name = f'Timescan: {scanfile}'
        root = Toplevel(parent)

        tk_widget = FELion_Toplevel(root, title_name, location)

        fig, canvas = tk_widget.figure(dpi, figsize=(15, 5))
        ax = fig.add_subplot(111)

        frame = tk_widget.get_widget_frame()

        log = BooleanVar()
        log_btn = ttk.Checkbutton(frame, text='Log', variable=log)
        log_btn.place(relx=0.1, rely=0.3, relwidth=0.5, relheight=0.05)
        log.set(False)

        ####################################### PLOTTING DETAILS #######################################

        tk_widget.check_button_maker(masslist, x=0.1, y=0.5)

        def plot():
            mass_check = tk_widget.get_check_values()

            temp_mean, temp_error = [], []
            counter = 0
            for n, i in zip(iterations, masslist):

                if mass_check[i].get():
                    print(f'Plotting Mass: {i}\n')
                    lg = f'{i}[{n}]; B0: {t_b0}ms; Res: {t_res}'
                    ax.errorbar(time, m[f'{i}'],
                                m[f'e{i}'], fmt='.-', label=lg)

                    temp_mean.append(m[f'{i}'])
                    temp_error.append(m[f'e{i}'])

                    counter += 1

            temp_mean_with_error = unp.uarray(temp_mean, temp_error)
            temp_sum_mean_with_error = temp_mean_with_error.sum(axis=0)

            if counter > 1:
                ax.errorbar(time, unp.nominal_values(temp_sum_mean_with_error), unp.std_devs(
                    temp_sum_mean_with_error), fmt='--', label=f'SUM TOTAL', color='k')

            if log.get():
                ax.set_yscale('log')

            # figure details
            ax.set_title('Time Scan plot for %s' % scanfile)
            ax.set_xlabel('Time (ms)')
            ax.set_ylabel('Counts')
            ax.legend()
            ax.grid(True)

        def update():

            t0 = check_time()
            ax.clear()

            plot()
            canvas.draw()

            t1 = check_time()

            print(f'Redrawn in {(t1-t0)*100:.2f} ms')

        update_btn = ttk.Button(
            frame, text='Update Plot', command=lambda: update())
        update_btn.place(relx=0.2, rely=0.4, relwidth=0.5, relheight=0.05)

        plot()

        ####################################### END Plotting details #######################################

        canvas.draw()

        ####################################### END Tkinter figure #######################################

        t1 = check_time()
        print(f'Timescan plot completed in {(t1-t0)*100:.2f} ms\n')

    except:
        ErrorInfo('Error: ', traceback.format_exc())
