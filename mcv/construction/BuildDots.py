import tkinter as tk
from tkinter import messagebox
import csv
import os

class MyButton(tk.Button):
    def __init__(self, master=None, x=0, y=0, **kwargs):
        super().__init__(master, **kwargs)
        self.x = x
        self.y = y

class BuildDots(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Building dots")
        self.tiles = [[None for _ in range(28)] for _ in range(36)]
        self.grid()
        self.create_widgets()
        self.load_walls()
        self.geometry(f"{224*3}x{288*3}")
        self.resizable(False, False)

    def create_widgets(self):
        for i in range(36):
            for j in range(28):
                btn = MyButton(self, x=i, y=j, bg="black", command=lambda b=btn: self.on_button_click(b))
                btn.grid(row=i, column=j)
                self.tiles[i][j] = btn

    def load_walls(self):
        try:
            with open("src/construction/walls.csv", "r") as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    i, j = int(row[0]), int(row[1])
                    self.tiles[i][j].config(bg="blue")
        except FileNotFoundError:
            messagebox.showerror("Error", "walls.csv file not found")

    def on_button_click(self, button):
        button.config(bg="red")
        try:
            with open("src/construction/dots.csv", "a", newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([button.x, button.y])
        except IOError as e:
            messagebox.showerror("Error", f"Failed to write to dots.csv: {e}")

if __name__ == "__main__":
    if not os.path.exists("src/construction/dots.csv"):
        with open("src/construction/dots.csv", "w") as f:
            pass
    app = BuildDots()
    app.mainloop()