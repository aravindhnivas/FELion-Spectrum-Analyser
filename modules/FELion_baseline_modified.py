#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os

def felix_read_file(felixfile):
    file = np.genfromtxt(felixfile)
    wn, count, sa = file[:,0], file[:,2], file[:,3]
    data = wn, count, sa
    data = np.take(data, data[0].argsort(), 1)
    return data

def ReadBase(basefile):

    #Opening basefile and taking the first two column which is wavenumber and its counts
    file = np.genfromtxt(basefile)
    wl, cnt = file[:,0], file[:,1]

    #the second line in the base file must have #BTYPE=
    with open(basefile) as f:
        interpol = f.readlines()[1].strip().split('=')[-1]

    return wl, cnt, interpol
