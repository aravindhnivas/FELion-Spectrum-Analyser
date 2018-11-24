from tkinter import *

#Defining root frame window
root = Tk()
# You can't drag the windows corner's to maximize or minimize the window
width_window = 1000
height_window = 500
#To make the window appear in the center:
your_computer_screen_width = root.winfo_screenwidth()
your_computer_screen_height = root.winfo_screenheight()
x_coordinate = (your_computer_screen_width/2) - (width_window/2) 
y_coordinate = (your_computer_screen_height/2) - (height_window/2)
root.geometry("%dx%d+%d+%d" %(width_window, height_window, x_coordinate, y_coordinate))
#root.geometry("%dx%d+%d+%d" %(width_window, height_window, \
  #  your_computer_screen_width/2, your_computer_screen_height/2))

root.resizable(width=FALSE, height=FALSE)

root.mainloop()