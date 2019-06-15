import matplotlib.pyplot as plt
import numpy as np
import os

filelist = []
fnames = os.listdir()

for i in fnames:
    if i.find(".dat")>=0:
        filelist.append(i)
        
for i in filelist:
    x, y = np.loadtxt(i, delimiter='\t', unpack=True)
    plt.plot(x,y, label=i)

plt.xlabel('Wavelength(cm-1)')
plt.ylabel('Intensity')
plt.title('Graph')
plt.legend()
plt.show()