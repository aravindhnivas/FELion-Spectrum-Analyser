#!/usr/bin/python3

import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.optimize import curve_fit
from FELion_definitions import ShowInfo, ErrorInfo


def timescanplot(fname, location, save, show, depletion=False):

    try:

        os.chdir(location)

        var = {'res':'m03_ao13_reso', 'b0':'m03_ao09_width'}
        print(var)

        with open(fname, 'r') as f:
            f = np.array(f.readlines())
        for i in f:
            if not len(i.strip())==0 and i.split()[0]=='#':
                for j in var:
                    if var[j] in i.split():
                        var[j] = float(i.split()[-3])

        t_res, t_b0 = round(var['res']), int(var['b0']/1000)
        print(var)

        with open(fname, 'r') as f: file = f.readlines()
        
        skip = [num for num, line in enumerate(file) if 'ALL:' in line.split()]
        iterations = np.array([int(i.split()[-1]) for i in file if not len(i.strip())==0 and i.split()[0].startswith('#mass')])
        length = len(iterations)

        data = np.genfromtxt(fname, skip_header = skip[0]+1)

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
            
        mean = [[np.array(temp2[i][j]).mean() for j in range(cycle)]for i in range(length)]
        error = [[(np.array(temp2[i][j]).std()) for j in range(cycle)]for i in range(length)]
        mass, mean, error = np.array(mass), np.array(mean), np.array(error)

        if depletion: return mass, iterations, t_res, t_b0,  mean, error, time

        plt.figure(figsize=(15,5), dpi=100)

        for i in range(length):
            lg = "%.2f:[%i]; B0: %i ms, Res: %i"%(mass[i], iterations[i], t_b0, t_res)
            plt.errorbar(time, mean[i],error[i],fmt='.-', label = lg)
            
        plt.title('Time Scan plot for %s'%fname)
        plt.xlabel('Time (ms)')
        plt.ylabel('Counts')
        plt.legend()
        plt.tight_layout()

        if save:
            file = fname.split('.')[0]
            plt.savefig(file+'.png')
            ShowInfo('Saved', 'File Saved as %s.png'%file)
        if show: plt.show()
        
        plt.close()

    except Exception as e:
        ErrorInfo("ERROR", e)