import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter
from Okno import Okno



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Football stats")
        self.center_window()
        Okno(self)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()   

        x = (screen_width // 2) - (1250 // 2)
        y = (screen_height // 2) - (750 // 2)

        self.geometry(f'1250x750+{x}+{y}')

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = App()
app.mainloop()