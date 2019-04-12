from tkinter import Toplevel, Tk, messagebox

def on_closing():
    
    if messagebox.askokcancel('Do you want to quit?'):
        root.quit()
        root.destroy()

root = Tk()
root.title('Main')
root.withdraw()

top = Toplevel(master=root)
top.title('Top')

top.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

