import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master=None, x=0, y=0, **kwargs):
        super().__init__(master, **kwargs)
        self.x = x
        self.y = y