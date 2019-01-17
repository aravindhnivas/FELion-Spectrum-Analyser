import tkinter as tk
class CustomWidget(tk.Frame):
    def __init__(self, parent, label, default="", strng):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text=label, anchor="w")
        self.entry = tk.Entry(self)
        
        self.strng = strng
        if self.strng: self.value = StrngVar()
        else: sefl.value = IntVar()
        
        self.entry.insert(0, default)

        self.label.pack(side="top", fill="x")
        self.entry.pack(side="bottom", fill="x", padx=4)

    def get(self):
        return self.entry.get()

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.e1 = CustomWidget(self, "First Name:", "Inigo")
        self.e2 = CustomWidget(self, "Last Name:", "Montoya")

        self.e1.grid(row=0, column=0, sticky="ew")
        self.e2.grid(row=1, column=0, sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).place(x=0, y=0, relwidth=1, relheight=0.3)
    root.mainloop()