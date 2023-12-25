import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter
from Okno import Okno


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Football stats")
        Okno(self)

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = App()
app.mainloop()