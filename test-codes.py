 mass_fileList = []

        def popupinput():
            pop = Tk()
            pop.geometry("400x400")

            pop_label = Label(pop, text = "Enter the mass_spec file names (comma separated): ", font=("Times", 10, "bold"))
            pop_label.pack()
            
            pop_input = StringVar()

            pop_entry = Entry(pop, bg = "white", bd = 5, textvariable = pop_input, justify = LEFT, font=("Times", 10, "bold"))
            pop_input.set("Enter here")
            pop_entry.focus_set()
            pop_entry.pack()

            done_button = ttk.Button(pop, text = "DONE", command = lambda: pop.quit())
            done_button.pack()

            fileList = pop_input.get()
            pop.mainloop()
            
            return fileList.split(",")
        
        display_label = Label(bottomFrame, font=("Times", 10, "italic"))