## A simple GUI program for FELion Instrument:

from tkinter import *
from tkinter import messagebox

# User defined definitions:
def on_closing():
  if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.destroy()

#Creating a class and also inheriting another class Tk() from tkinter
class FELion(Tk):

  def __init__(self, *args, **kwargs):
    #Initialsing parameters from the inherited class Tk() from tkinter:
    Tk.__init__(self, *args, **kwargs)
    container = Frame(self)
    container.pack(side = "top", fill = "both", expand = True)
    pass

root = FELion()

root.mainloop()

##TEMP
'''
root = Tk()
#Defining the main window's dimensions:
width_window = 700
height_window = 500
#Making window appear at the center of your computer screen:
your_computer_screen_width = root.winfo_screenwidth()
your_computer_screen_height = root.winfo_screenheight()
x_coordinate = (your_computer_screen_width/2) - (width_window/2) 
y_coordinate = (your_computer_screen_height/2) - (height_window/2)
root.geometry("%dx%d+%d+%d" %(width_window, height_window, x_coordinate, y_coordinate))
#Defining the window titile
root.title("FELion Spectrum Analyser")
#Configuring window
root.config()
'''