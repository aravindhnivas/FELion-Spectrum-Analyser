#!/usr/bin/python3

# Built-In modules
import os

# DATA analysis modules
import numpy as np

####################################### Modules Imported #######################################

def var_find(fname, location, time = False):
    #print(f'###############\nFile: {fname}\nLocation: {location}\n###############')

    if not fname is '':
        os.chdir(location)
        if not time: var = {'res':'m03_ao13_reso', 'b0':'m03_ao09_width', 'trap': 'm04_ao04_sa_delay'}
        else: var = {'res':'m03_ao13_reso', 'b0':'m03_ao09_width'}

        #print(var)

        with open(fname, 'r') as f:
            f = np.array(f.readlines())
        for i in f:
            if not len(i.strip())==0 and i.split()[0]=='#':
                for j in var:
                    if var[j] in i.split():
                        var[j] = float(i.split()[-3])

        if not time: res, b0, trap = round(var['res'], 1), int(var['b0']/1000), int(var['trap']/1000)
        else: res, b0 = round(var['res'], 1), int(var['b0']/1000)
        #print(var)

        if time: return res, b0

        return res, b0, trap
    else:
        if time: return 0, 0
        return 0, 0, 0

# Timescan plot
def get_skip_line(scanfile, location):
    os.chdir(location)
    with open(scanfile, 'r') as f:
        skip = 0
        for line in f:
            if len(line)>1:
                line = line.strip()
                if line == 'ALL:':
                    #print(f'\n{line} found at line no. {skip+1}\n')
                    return skip + 1
            skip += 1
    return f'ALL: is not found in the file'

def get_iterations(scanfile, location):
    os.chdir(location)
    iterations = np.array([])
    with open(scanfile, 'r') as f:
        for line in f:
            if line.startswith('#mass'):
                #print(line)
                iterations = np.append(iterations, line.split(':')[-1]).astype(np.int64)
            else: continue
    return iterations

def timescanplot(scanfile, location):

    '''
    return time, m, masslist, iterations, t_res, t_b0
    '''

    ####################################### Initialisation #######################################
    os.chdir(location)

    skip = get_skip_line(scanfile, location)
    iterations = get_iterations(scanfile, location)

    # opening File
    data = np.genfromtxt(scanfile, skip_header = skip)

    # Calculating the time step cycle and total no of masses (run)
    cycle = int(len(data)/iterations.sum())
    run = len(iterations)

    # Time
    time = data[:, 1][: cycle]

    # Calculating mean and std_devs
    j = 0
    mean, error = [], []
    mass = []
    m = {}

    for num, iteration in enumerate(iterations):
        
        k = iteration*cycle

        
        mass_value = data[:, 0][j:k+j][0]
        mass_sort = data[:, 2][j:k+j].reshape(iteration, cycle).mean(axis = 0)
        error_sort = data[:, 2][j:k+j].reshape(iteration, cycle).std(axis = 0)
        
        mass = np.append(mass, mass_value)
        mean = np.append(mean, mass_sort)
        error = np.append(error, error_sort)

        m[f'{mass_value}'] =  mass_sort
        m[f'e{mass_value}'] = error_sort
        
        j = k + j

    mean = mean.reshape(run, cycle)
    error = error.reshape(run, cycle)

    # Getting B0 width and Mass resolution from Timescan file
    t_res, t_b0 = var_find(scanfile, location, time = True)

    masslist = mass.astype(str)
    return time, m, masslist, iterations, t_res, t_b0