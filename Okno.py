import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter

from OknoStartowe import OknoStartowe
from OknoLigowe import OknoLigowe

class Okno:
    def __init__(self, root):
        self.root = root
        self.aktywneOkno = OknoStartowe(self.root, self)
    
    def clearFrame(self):
       for widgets in self.root.winfo_children():
          widgets.destroy()
          
    def setView(self, view):
        self.clearFrame()
        del self.aktywneOkno
        
        if view == "ligowe":
            self.aktywneOkno = OknoLigowe(self.root, self)
        elif view == "menuStartowe":
            self.aktywneOkno = OknoStartowe(self.root, self)

      

