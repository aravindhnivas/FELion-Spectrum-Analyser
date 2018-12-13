# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

from tkinter import *
from tkinter import ttk, messagebox
import os
import shutil

#FELion modules
from FELion_massSpec import massSpec

def locationnotfound(location):
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", "Location NOT FOUND".format(location))
        root.destroy()

def outFile(fname, location, file):
        try:
                os.chdir(location)
                my_path = os.getcwd()
                #file = T.get("1.0", "end-1c")


                def saveinfo():
                        os.chdir(location)
                        if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                                save = Tk()
                                save.withdraw()
                                messagebox.showinfo("Information", \
                                        "File {}.pow saved in /Pow directory".format(fname))
                                save.destroy()

                def write():
                        f = open(my_path+"/Pow/{}.pow".format(fname), "w")
                        f.write(file)
                        f.close()
                        saveinfo()

                
                if not os.path.isdir("Pow"):
                        os.mkdir("Pow")

                if os.path.isfile(my_path+"/Pow/{}.pow".format(fname)):
                        if messagebox.askokcancel("Overwrite", \
                                "Do yo want to overwrite the existing {}.pow file?".format(fname)):
                                write()
                                
                else:
                        write()

        except:
                locationnotfound(location)

LARGE_FONT= ("Verdana", 12)

diff = 0.15
x1 = 0.3
x2 = x1 + diff
x3 = x2 + diff

y = 0.9
width, height = (100, 40)
smallwidth = 50

class FELion(Tk):


    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        #Tk.iconbitmap(self,default='FELion_Icon.ico')
        Tk.wm_title(self, "FELion-Spectrum Analyser v.2.0")
        Tk.wm_geometry(self, "900x500")

        container = Frame(self)
        container.config(bg = "sea green")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        StatusBarFrame = Frame(self)
        StatusBarFrame.pack(side = "bottom", fill = "both", expand = False)

        statusBar_left_text = "Version 1.0"
        statusBar_left = Label(StatusBarFrame)
        statusBar_left.config(text = statusBar_left_text, \
        relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "w")
        statusBar_left.pack(side = "top", fill = "both", expand = True)

        statusBar_right_text = "Developed at FELIX"
        statusBar_right = Label(StatusBarFrame)
        statusBar_right.config(text = statusBar_right_text, \
        relief = SUNKEN, bd = 2, font = "Times 10 italic", pady = 5, anchor = "e")
        statusBar_right.pack(side = "top", fill = "both", expand = True)

        self.frames = {}

        for F in (StartPage, Normline, Mass, Powerfile):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        
        label = Label(self, text="Welcome", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Norm and Avg",
                            command=lambda: controller.show_frame(Normline))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Mass Spec",
                            command=lambda: controller.show_frame(Mass))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Powerfile",
                            command=lambda: controller.show_frame(Powerfile))
        button3.place(relx = x3, rely = y, width = width, height = height)


class Normline(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Norm and Avg!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Mass Spec",
                            command=lambda: controller.show_frame(Mass))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Powerfile",
                            command=lambda: controller.show_frame(Powerfile))
        button3.place(relx = x3, rely = y, width = width, height = height)


class Mass(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Mass Spec!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Norm and Avg",
                            command=lambda: controller.show_frame(Normline))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Powerfile",
                            command=lambda: controller.show_frame(Powerfile))
        button3.place(relx = x3, rely = y, width = width, height = height)

        # Mass Spectrum:
        massSpec_label = Label(self, text = "Mass_file: ", font=("Times", 10, "bold"))
        

        # the compund details:
        molecule_name_label = Label(self, text = "Molecule", font=("Times", 10, "bold"))
        temp_label = Label(self, text = "TEMP(K)", font=("Times", 10, "bold"))
        bwidth_label = Label(self, text = "B0 Width(ms)", font=("Times", 10, "bold"))
        ion_enrg_label = Label(self, text = "IE(eV)", font=("Times", 10, "bold"))

        mname = StringVar()
        temp = StringVar()
        bwidth = StringVar()
        ie = StringVar()

        mname.set("Molecule")
        temp.set("-")
        bwidth.set("-")
        ie.set("-")

        molecule_name = Entry(self, bg = "white", bd = 5, textvariable=mname, justify = LEFT, font=("Times", 12, "italic"))
        temperature = Entry(self, bg = "white", bd = 5, textvariable=temp, justify = LEFT, font=("Times", 12, "italic"))
        bo_Width = Entry(self, bg = "white", bd = 5, textvariable=bwidth, justify = LEFT, font=("Times", 12, "italic"))
        ion_enrg = Entry(self, bg = "white", bd = 5, textvariable=ie, justify = LEFT, font=("Times", 12, "italic"))

        mass = StringVar()
        mass.set("Enter here")
        massSpec_input = Entry(self, bg = "white", bd = 5, \
                textvariable=mass, justify = LEFT, font=("Times", 12, "italic"))
                
        mass_button = ttk.Button(self, text="MassSpec", \
                                        command = lambda: massSpec(\
                                        mass.get(), mname.get(), temp.get(), bwidth.get(), ie.get(),\
                                        mass_xmin.get(), mass_xmax.get(),\
                                        location.get(),\
                                        m_figwidth.get(), m_figheight.get(),\
                                        combine_entry_values.get(),\
                                        output_filename.get(),\
                                        mass_method_value.get(),\
                                        mass_saveCheck_value.get()
                                        )
                                )

        # Save checkbutton:
        mass_saveCheck_value = BooleanVar()
        mass_saveCheck_value.set(True)
        mass_saveCheck = ttk.Checkbutton(self, text = "Save", variable = mass_saveCheck_value)
        
        # Mass Spec labels:
        mass_range_label = Label(self, text = "Range(u):", font=("Times", 10, "bold"))

        mass_xmin = IntVar()
        mass_xmax = IntVar()
        mass_xmin.set(0)
        mass_xmax.set(80)
        mass_xmin_Entry = Entry(self, bg = "white", bd = 5, \
                textvariable=mass_xmin, justify = LEFT, font=("Times", 10, "bold"))
        mass_xmax_Entry = Entry(self, bg = "white", bd = 5, \
                textvariable=mass_xmax, justify = LEFT, font=("Times", 10, "bold"))

        mass_figsize = Label(self, text = "FigSize:", font=("Times", 10, "bold"))

        m_figwidth = IntVar()
        m_figheight = IntVar()

        m_figwidth.set(7)
        m_figheight.set(5)
        mass_figWidth = Entry(self, bg = "white", bd = 5, textvariable=m_figwidth, justify = LEFT, font=("Times", 10, "bold"))
        mass_figHeight = Entry(self, bg = "white", bd = 5, textvariable=m_figheight, justify = LEFT, font=("Times", 10, "bold"))

        
        

        #Combine Mass spec:
        def combine_func(self, combine):
                display_label = Label(self, font=("Times", 10, "italic"))

                if not combine:
                        display_label.config(text = "Single mode active:")
                        display_label.place(relx = 0.7,  rely = 0.5, relwidth = 0.2, height = 40)

                if combine:
                        display_label.config(text = "Combine mode active:")
                        display_label.place(relx = 0.7,  rely = 0.5, relwidth = 0.2, height = 40)
                


        mass_method_value = BooleanVar()
        single_mass = ttk.Radiobutton(self, text = "Single: ", \
                variable = mass_method_value, value = False, \
                command = lambda: combine_func(self, mass_method_value.get()))
        combine_mass = ttk.Radiobutton(self, text = "Combine: ", \
                variable = mass_method_value, value = True, \
                command = lambda: combine_func(self, mass_method_value.get()))

        
                

        combine_entry_values = StringVar()
        combine_entry_values.set("Combine: Enter just files nos. (if same data) comma separated")

        combine_entry = Entry(self, bg = "white", bd = 5,\
                                textvariable=combine_entry_values, justify = LEFT,\
                                font=("Times", 12, "italic"))

        
        mass_diff = 0.1
        mass_smalldiff = 0.5
        m_x1 = 0.1
        m_x2 = m_x1 + mass_diff
        m_x3 = m_x2 + mass_diff
        m_x4 = m_x3 + mass_diff
        m_y1 = 0.3
        m_y2 = m_y1 + mass_diff
        m_y3 = m_y2 + mass_diff
        m_y4 = m_y3 + mass_diff

        molecule_name_label.place(relx = m_x1,  rely = m_y1, width = width, height = height)
        temp_label.place(relx = m_x1,  rely = m_y2, width = width, height = height)
        bwidth_label.place(relx = m_x1,  rely =m_y3, width = width, height = height)
        ion_enrg_label.place(relx = m_x1,  rely = m_y4, width = width, height = height)
        molecule_name.place(relx = m_x2,  rely = m_y1, width = width, height = height)
        temperature.place(relx = m_x2,  rely =m_y2, width = width, height = height)
        bo_Width.place(relx = m_x2,  rely = m_y3, width = width, height = height)
        ion_enrg.place(relx = m_x2,  rely =m_y4, width = width, height = height)

        massSpec_label.place(relx = 0.1,  rely = 0.1, width = width, height = height)
        massSpec_input.place(relx = 0.2,  rely = 0.1, width = width, height = height)
        mass_range_label.place(relx = 0.7,  rely = 0.2, width = width, height = height)
        mass_xmin_Entry.place(relx = 0.8,  rely = 0.2, width = smallwidth, height = height)
        mass_xmax_Entry.place(relx = 0.85,  rely = 0.2, width = smallwidth, height = height)
        mass_figsize.place(relx = 0.7,  rely = 0.3, width = width, height = height)
        mass_figWidth.place(relx = 0.8,  rely = 0.3, width = smallwidth, height = height)
        mass_figHeight.place(relx = 0.85,  rely = 0.3, width = smallwidth, height = height)

        single_mass.place(relx = 0.7,  rely = 0.4, width = width, height = height)
        combine_mass.place(relx = 0.8,  rely = 0.4, width = width, height = height)

        combine_entry.place(relx = 0.7,  rely = 0.6, relwidth = 0.2, height = 50)

        mass_saveCheck.place(relx = 0.7,  rely = 0.7, width = width, height = height)
        mass_button.place(relx = 0.8,  rely = 0.7, width = width, height = height)



class Powerfile(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Powerfile Generator!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx = x1, rely = y, width = width, height = height)

        button2 = ttk.Button(self, text="Norm and Avg",
                            command=lambda: controller.show_frame(Normline))
        button2.place(relx = x2, rely = y, width = width, height = height)

        button3 = ttk.Button(self, text="Mass Spec",
                            command=lambda: controller.show_frame(Mass))
        button3.place(relx = x3, rely = y, width = width, height = height)

        # Labels and buttons:

        # Location:
        location_label = Label(self, text = "Location:", font=("Times", 10, "bold"))

        location = StringVar()
        location.set("Enter file lcoation here")
        location_entry = Entry(self, bg = "white", bd = 5,\
                                textvariable=location, justify = LEFT,\
                                font=("Times", 12, "italic"))

        #Label for Entry Box;
        user_input_label = Label(self, text = "Filename:", font=("Times", 10, "bold"))

        #Entry Box;
        init_msg = "Enter here" #initialising message
        content = StringVar()   #defining Stringvar()
        user_input = Entry(self, bg = "white", bd = 5, textvariable=content, justify = LEFT)
        user_input.config(font=("Times", 12, "italic"))
        user_input.focus_set()
        content.set(init_msg)

        #Baseline
        save_button = ttk.Button(self, text="Save")
        save_button.config(command = lambda: outFile(content.get(), location.get(), T.get("1.0", "end-1c")))

        T = Text(self)
        S = Scrollbar(self)
        T.config(yscrollcommand=S.set)
        S.config(command=T.yview)
        
        quote = """#POWER file\n# 10 Hz FELIX\n#\n#SHOTS=26\n#INTERP=linear\n#    IN_no_UM (if one deletes the "no" the firs number will be in \mu m\n# wavelength/cm-1      energy/pulse/mJ\n"""
        T.insert(END, quote)

        location_label.place(relx = 0.1,  rely = 0.1, width = 100, height = 40)
        user_input_label.place(relx = 0.1,  rely = 0.3, width = 100, height = 40)
        T.place(relx = 0.1,  rely = 0.5, relwidth = 0.7, relheight = 0.4)
        location_entry.place(relx = 0.3,  rely = 0.1, relwidth = 0.5, height = 40)
        user_input.place(relx = 0.3,  rely = 0.3, width = 100, height = 40)
        save_button.place(relx = 0.5,  rely = 0.3, width = 100, height = 40)
        S.place(relx = 0.8,  rely = 0.5, width = 15, relheight = 0.4)
        
app = FELion()
app.mainloop()