import tkinter as tk
from tkinter import ttk, StringVar, IntVar

class LabelAndEntry(tk.Frame):
    def __init__(self, parent, label, entry, strng):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text=label, font = ("Times", 12, "bold"))
        
        self.strng = strng
        if self.strng: self.value = StringVar()
        else: self.value = IntVar()
        
        self.value.set(entry)       
        
        self.entry = tk.Entry(self, textvariable = self.value, bg = "white",\
                              bd = 5, font = ("Times", 12, "italic"))

        self.label.grid(row = 0, column = 0)
        self.entry.grid(row = 0, column = 1)

    def get(self):
        return self.value.get()

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.e1 = LabelAndEntry(self, "Name:","John Nash", strng = True)
        self.e1.pack()
        
        self.e2 = LabelAndEntry(self, "Filename:","Hello "+ self.e1.get(), strng = True)
        self.e2.pack()

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack()
    root.mainloop()