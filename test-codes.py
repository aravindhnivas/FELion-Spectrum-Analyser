from tkinter import *

#Defining root frame window
root = Tk()

# Defining frames
topFrame = Frame(root, bg = "white", width=300, height=200)
bottomFrame = Frame(root, bg = "green")
label = Label(topFrame,\
              text = "FELion Spectrum Analyser",\
              bg = "green",\
              width=30, height=1,\
              font=("Courier", 30))

#Packing franes
topFrame.pack(fill = X)
bottomFrame.pack(side = BOTTOM,fill=X)
label.pack()

#Defining buttons:

#Defining input file name:
def retrieve_input():
    inputValue=textBox.get()
    file = str(inputValue)
    if file == "":
        print()
        print("###############################################################")
        print("Please enter the file name in the white box and click submit.")
        print("###############################################################")
    else:
        print()
        print("###############################################################")
        print("The file name is: {}".format(file))
        print("###############################################################")
    #return file

buttonInput=Button(bottomFrame,\
                   height=1, width=10,\
                   text="Submit",\
                   command = lambda: retrieve_input())
buttonInput.pack(side = RIGHT, padx=2, pady=2)
textBox=Entry(bottomFrame)
textBox.pack()

#Baseline
baseline_button = Button(bottomFrame, text="Baseline", width=20, height=1)
baseline_button.bind("<Button-1>",lambda: print("Hello"))
baseline_button.pack(side = TOP, padx=2, pady=2)

#Normline
normline_button = Button(bottomFrame, text="Normline", width=20, height=1)
normline_button.bind("<Button-1>", lambda: print("Hello"))
normline_button.pack(side = TOP, padx=2, pady=2)

#Avg_Spectrum
avg_button = Button(bottomFrame, text="Avg_spectrum", width=20, height=1)
avg_button.bind("<Button-1>", lambda: print("Hello"))
avg_button.pack(side = TOP, padx=2, pady=2)


#Creating a stable window to stat untill closed
root.mainloop()