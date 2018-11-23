#!/usr/bin/python3

#Importing all the required definitions from various functions
from tkinter import *
from FELion_baseline import *
from FELion_normline import *
from FELion_avgSpec import *

#custom import
import os
import shutil

#Defining the baseline_correction function for GUI button
def baseline_correction(event, fname=""):
    my_path = os.getcwd()

    if fname == "":
        fname = retrieve_input()
    if os.path.isdir('EXPORT'):
        print("EXPORT folder exist")
    else:
        os.mkdir('EXPORT')
        print("EXPORT folder created.")
        
    if os.path.isdir('OUT'):
        print("OUT folder exist")
    else:
        os.mkdir('OUT')
        print("OUT folder created.")

    if os.path.isdir('DATA'):
        print("DATA folder exist")
    else:
        os.mkdir('DATA')
        print("DATA folder created.")

    filename = fname + ".felix"

    if os.path.isfile(filename):
        print("File exist, Copying to the DATA folder to process.")
        shutil.copyfile(my_path + r"\{}".format(filename), my_path + r"\DATA\{}".format(filename))

    data = felix_read_file(fname)

    #Check wether the baslien file exists
    if not os.path.isfile('DATA/'+fname+'.base'):
        print("Guessing baseline from .felix file!")
        xs, ys = GuessBaseLine(data)
    else:
        print("Reading baseline from .base file!")
        xs, ys, *rest = ReadBase(fname)

    fig, ax = plt.subplots()

    p = InteractivePoints(fig, ax, xs, ys)
    ax.plot(data[0], data[1], ls='', marker='o', ms=5, markeredgecolor='r', c='r')

    print("\nUSAGE:\nBlue baseline points are dragable...\
           \nKeys:\n\
    'a' - adds a point at current cursor position\n\
    'd' - delets a point at current cursor position\n\
    'w' - moves the point to the 'average' value at given x position\n\
    'q' - stores baseline in .base file and quits!\n")

    ax.set_title('BASELINE points are drag-able!')
    ax.set_xlim((data[0][0]-70, data[0][-1]+70))
    ax.set_xlabel("wavenumber (cm-1)")
    ax.set_ylabel("Counts")
    plt.show()
    
    #Powerfile check
    powerfile = fname + ".pow"
    if not os.path.isfile(powerfile):
        print("NOTE: You don't have .pow file so you can't plot the data yet but you can make the baseline.")
    elif os.path.isfile(powerfile):
        shutil.copyfile(my_path + r"\{}".format(powerfile), my_path + r"\DATA\{}".format(powerfile))
        print("Powerfile is copied to the DATA folder")

    if baseline != None:
        SaveBase(fname, baseline)
    return

#Defining Button Actions

#Defining Normline
def normline(event, fname="",s = True, plotShow = False):
    my_path = os.getcwd()
    if fname == "":
        fname = retrieve_input()
        full_fname = fname + ".felix"
        powerfile = fname + ".pow"
    if os.path.isfile(powerfile):
        shutil.copyfile(my_path + r"\{}".format(powerfile), my_path + r"\DATA\{}".format(powerfile))
        print("Powerfile copied to the DATA folder.")
    else:
        print("\nCAUTION:You don't have the powerfile(.pow)\n")

    a,b = norm_line_felix(fname, save=s, show=plotShow)
    print("\nProcess Completed.\n")
    return

#Defining Average Spectrum function
def avgSpec(event, t="Title", ts=10, lgs=5, \
        minor=5, major=50, majorTickSize=8, \
        xmin=1000, xmax=2000):

    fig = plt.subplot(1,1,1)
    plt.rcParams['figure.figsize'] = [6,4]
    plt.rcParams['figure.dpi'] = 80
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['font.size'] = ts # Title Size
    plt.rcParams['legend.fontsize'] = lgs # Legend Size

    my_path = os.getcwd() # getting current directory
    pwd = os.listdir(my_path + r"\DATA") # going into the data folder to fetch all the available data filename.
    fileNameList = [] # creating a varaiable list : Don't add any data here. You can use the script as it is since it automatically takes the data in the DATA folder
    for p in pwd:
        if p.endswith(".felix"): # finding the files only with .felix extension
            filename = os.path.basename(p) # getting the name of the file
            file = os.path.splitext(filename)[0] # printing only the file name without the extension .felix
            fileNameList.append([file]) # saving all the file names in the variable list fileNameList
        else:
            continue
            
    xs = np.array([],dtype='double')
    ys = np.array([],dtype='double')

    for l in fileNameList:
        a,b = norm_line_felix(l[0])
        fig.plot(a, b, ls='', marker='o', ms=1, label=l[0])
        xs = np.append(xs,a)
        ys = np.append(ys,b)
    fig.legend(title=t) #Set the fontsize for each label

    #Binning
    binns, inten = felix_binning(xs, ys, delta=DELTA)
    fig.plot(binns, inten, ls='-', marker='', c='k')

    #Exporting the Binned file.
    F = 'OUT/average_Spectrum.pdf'
    export_file(F, binns, inten)

    #Set the Xlim values and fontsizes.
    fig.set_xlim([xmin,xmax])
    fig.set_xlabel(r"Calibrated lambda (cm-1)", fontsize=10)
    fig.set_ylabel(r"Normalized Intensity", fontsize=10)
    fig.tick_params(axis='both', which='major', labelsize=majorTickSize)

    #Set the Grid value False if you don't need it.
    fig.grid(True)
    #Set the no. of Minor and Major ticks.
    fig.xaxis.set_minor_locator(MultipleLocator(minor))
    fig.xaxis.set_major_locator(MultipleLocator(major))
    plt.savefig(F)
    plt.close()
    print()
    print("Completed.")
    print()
    return

#Assigning the spectrum functions:
b = baseline_correction
n = normline
a = avgSpec

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
    inputValue=textBox.get("1.0","end-1c")
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
    return file

buttonInput=Button(bottomFrame,\
                   height=1, width=10,\
                   text="Submit",\
                   command = retrieve_input)
buttonInput.pack(side = RIGHT, padx=2, pady=2)
textBox=Text(bottomFrame, width=10, height=2)
textBox.pack(side = RIGHT)

#Baseline
baseline_button = Button(bottomFrame, text="Baseline", width=20, height=1)
baseline_button.bind("<Button-1>", b)
baseline_button.pack(side = TOP, padx=2, pady=2)

#Normline
normline_button = Button(bottomFrame, text="Normline", width=20, height=1)
normline_button.bind("<Button-1>", n)
normline_button.pack(side = TOP, padx=2, pady=2)

#Avg_Spectrum
avg_button = Button(bottomFrame, text="Avg_spectrum", width=20, height=1)
avg_button.bind("<Button-1>", a)
avg_button.pack(side = TOP, padx=2, pady=2)

#Save Button
def save(event):
    global root
    root.quit()

saveButton = Button(bottomFrame, text="Save", fg = "green", width=10, height=1)
saveButton.bind("Button-1", save)
saveButton.pack()

#Quit Button
def destroy():
    global root
    root.destroy()

quitButton = Button(bottomFrame, text="Quit", fg = "red", command=destroy).pack()

#Root mainloop
root.mainloop()

print("###############################################################")
print("\n\nProgram closed.\n\n")
print("###############################################################")
#EXIT