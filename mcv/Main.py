from Model import Model
from EventManager import EventManager
from Table import Table
import tkinter as tk

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    model = Model()
    event_manager = EventManager()
    grafica = Table(root)

    grafica.set_event_manager(event_manager)
    event_manager.set_model(model)
    event_manager.set_table(grafica)

    root.deiconify()  # Show the root window
    root.mainloop()  # Call mainloop on the root window

if __name__ == "__main__":
    main()