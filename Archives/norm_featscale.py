import matplotlib.pyplot as plt
import os

filelist = []
fnames = os.listdir()

for i in fnames:
    if i.find(".dat")>=0:
        filelist.append(i)

def makeint(filename):
    a, b, aint, bint = [],[],[],[]
    f = open(filename)
    for i in f:
        if not i[0] == "#" and not i == "\n":
            a1, b1 = i.split()
            a.append(a1)
            b.append(b1)
    for i, j in zip(a, b):
        i, j = float(i), float(j)
        aint.append(i)
        bint.append(j)
        
    norma, normb = [], []
    
    # normalising (Feature Scaling (0,1) range):
    for i, j in zip(aint, bint):
        i = (i-min(aint))/(max(aint)-min(aint))
        norma.append(i)
        j = (j-min(bint))/(max(bint)-min(bint))
        normb.append(j)
    
    f.close()
        
    return norma, normb

for f in filelist:
    x, y = makeint(f)
    plt.plot(x, y, label = f)
    
plt.xlabel('x')
plt.ylabel('y')
plt.title('Graph')
plt.legend()
plt.show()
plt.close()