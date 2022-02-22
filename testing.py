from tkinter import *


def check_key(event):
    print(f"{event.keysym}; {event}")


root = Tk()
root.geometry("0x0")
root.bind("<Key>", check_key)
root.mainloop()
