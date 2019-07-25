
# Importing Modules

# System modules
import sys, json, os
from os.path import isdir, isfile
from pathlib import Path as pt

# Data analysis
import numpy as np
from uncertainties import unumpy as unp


####################################### Modules Imported #######################################

class timescanplot:

    def __init__(self, scanfile, location):

        os.chdir(location)

        skip = get_skip_line(scanfile, location)
        iterations = get_iterations(scanfile, location)

        # opening File
        data = np.genfromtxt(scanfile, skip_header=skip)

        cycle = int(len(data)/iterations.sum())
        run = len(iterations)
        time = data[:, 1][: cycle]

        # Calculating mean and std_devs
        j = 0
        mean, error = [], []
        mass = []
        m = {}
        for iteration in iterations:
            k = iteration*cycle

            mass_value = data[:, 0][j:k+j][0]
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

        mean = mean.reshape(run, cycle)
        error = error.reshape(run, cycle)

        t_res, t_b0 = var_find(scanfile, location, time=True)
        masslist = mass.astype(str)

        temp_mean, temp_error = [], []

        for mass in masslist:
            temp_mean.append(m[f'{mass}'])
            temp_error.append(m[f'e{mass}'])

        temp_mean_with_error = unp.uarray(temp_mean, temp_error)
        temp_sum_mean_with_error = temp_mean_with_error.sum(axis=0)

        dataJson = json.dumps(m)
        print(dataJson)

def var_find(fname, location, time=False):
    print(
        f'###############\nFile: {fname}\nLocation: {location}\n###############')

    if not fname is '':
        os.chdir(location)
        if not time:
            var = {'res': 'm03_ao13_reso', 'b0': 'm03_ao09_width',
                   'trap': 'm04_ao04_sa_delay'}
        else:
            var = {'res': 'm03_ao13_reso', 'b0': 'm03_ao09_width'}

        print(var)

        with open(fname, 'r') as f:
            f = np.array(f.readlines())
        for i in f:
            if not len(i.strip()) == 0 and i.split()[0] == '#':
                for j in var:
                    if var[j] in i.split():
                        var[j] = float(i.split()[-3])

        if not time:
            res, b0, trap = round(var['res'], 1), int(
                var['b0']/1000), int(var['trap']/1000)
        else:
            res, b0 = round(var['res'], 1), int(var['b0']/1000)
        print(var)

        if time:
            return res, b0

        return res, b0, trap
    else:
        if time:
            return 0, 0
        return 0, 0, 0

def get_skip_line(scanfile, location):

    os.chdir(location)
    with open(scanfile, 'r') as f:
        skip = 0
        for line in f:
            if len(line) > 1:
                line = line.strip()
                if line == 'ALL:':
                    print(f'\n{line} found at line no. {skip+1}\n')
                    return skip + 1
            skip += 1
    return f'ALL: is not found in the file'

def get_iterations(scanfile, location):

    os.chdir(location)
    iterations = np.array([])
    with open(scanfile, 'r') as f:
        for line in f:
            if line.startswith('#mass'):
                print(line)
                iterations = np.append(
                    iterations, line.split(':')[-1]).astype(np.int64)
            else:
                continue
    return iterations

if __name__ == "__main__":

    args = sys.argv[1:][0].split(",")
    filepaths = args
    location = pt(filepaths[0]).parent

    #print(f"Files: {filepaths}\nLocation: {location}")
    timescanplot(filepaths, location)