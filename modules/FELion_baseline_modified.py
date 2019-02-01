#!/usr/bin/python3
import numpy as np

def felix_read_file(felixfile):

    file = np.genfromtxt(felixfile)
    wn, count, sa = file[:,0], file[:,2], file[:,3]
    data = wn, count, sa
    data = np.take(data, data[0].argsort(), 1)
    return data

def ReadBase(basefile):

    file = np.genfromtxt(basefile)
    wl, cnt = file[:,0], file[:,1]
    with open(basefile, 'r') as f:
        interpol = f.readlines()[1].strip().split('=')[-1]
    return wl, cnt, interpol
