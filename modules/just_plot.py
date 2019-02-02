
import matplotlib.pyplot as plt
import numpy as np
import os


def theory_exp(theory,exp, location, save, show):

    os.chdir(location)
    
    t = np.genfromtxt(theory, comments='F')
    e = np.genfromtxt(exp)
    xt, yt, xe, ye = t[:,0], t[:,1], e[:,0], e[:,1]
    yt = (yt/yt.max())*ye.max()

    plt.figure(dpi=100)

    plt.vlines(xt, ymin=0, ymax=yt, lw = 5, label = 'Theory')
    plt.plot(xe,ye, label='Exp')

    plt.legend()
    plt.title('Theory vs Exp: %s'%exp)
    plt.xlabel('Wavenumber $cm^{-1}$')
    plt.ylabel('Normalised Intensity \n(Theory Inten. is norm. to Exp.)')
    plt.xlim(xmax = xe.max(), xmin = xe.min())
    plt.ylim(ymin=0)
    plt.tight_layout()
    if save: plt.savefig('theory-exp_%s.png'%exp.split('.')[0])
    if show: plt.show()
    plt.close()