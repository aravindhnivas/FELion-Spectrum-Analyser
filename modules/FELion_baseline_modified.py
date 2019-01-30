

import numpy as np

def felix_read_file(fname):
    file = np.genfromtxt(fname)
    wn, count, sa = file[:,0], file[:,2], file[:,3]
    data = wn, count, sa
    data = np.take(data, data[0].argsort(), 1)
    return data