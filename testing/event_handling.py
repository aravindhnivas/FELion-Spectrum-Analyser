
import matplotlib.pyplot as plt
import os
import numpy as np


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))


fig, axs = plt.subplots(1,1)
axs.plot(np.random.rand(10))
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()