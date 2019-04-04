# draggable rectangle with the animation blit techniques; see

import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np


class DraggableRectangle:
    lock = None  # only one can be animated at a time
    def __init__(self, rect, canvas):
        self.canvas = canvas
        self.rect = rect
        self.press = None
        self.background = None
    
    def connect(self):
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and then store some data'
        
        # Clicking outside the plot region just return
        if event.inaxes is None: return

        if DraggableRectangle.lock is not None: return

        contains, attrd = self.rect.contains(event)

        if not contains: return
        else: print('event contains', self.rect.xy)
        
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata
        print(self.press)
        DraggableRectangle.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        axes = self.rect.axes
        self.rect.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.rect.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.rect)

        # and blit just the redrawn area
        self.canvas.blit(axes.bbox)

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if DraggableRectangle.lock is not self: return
        if event.inaxes is None: return
        
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        print(f'\ndx: {dx}\ndy: {dy}\n')
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        axes = self.rect.axes
        
        # restore the background region
        self.canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.rect)

        # blit just the redrawn area
        self.canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableRectangle.lock is not self:
            return

        self.press = None
        DraggableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.rect.set_animated(False)
        self.background = None

        # redraw the full figure
        self.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.canvas.mpl_disconnect(self.cidpress)
        self.canvas.mpl_disconnect(self.cidrelease)
        self.canvas.mpl_disconnect(self.cidmotion)

def main():
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    fig = Figure(figsize = (10, 5), dpi = 100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

    rects = ax.bar(range(10), 20*np.random.rand(10))
    drs = []
    for rect in rects:
        dr = DraggableRectangle(rect, canvas)
        dr.connect()
        drs.append(dr)
        
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    tkinter.mainloop()

if __name__ == '__main__':
    main()