import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter


class OknoStartowe:
    def __init__(self, root, glowneOkno):
        self.root = root
        self.root.geometry("500x350")
        self.windowView() 
        self.glowneOkno = glowneOkno
    
    def windowView(self):
        self.przycisk_aktualizacji = customtkinter.CTkButton(master=self.root, text="Aktualizuj dane", command=self.aktualizuj_dane)
        self.przycisk_ustawien = customtkinter.CTkButton(master=self.root, text="Ustawienia", command=self.otworz_ustawienia)
        self.przycisk_dane_ligi = customtkinter.CTkButton(master=self.root, text="Dane ligi", command=self.otworz_dane_ligi)
        self.przycisk_wyszukaj_zawodnika = customtkinter.CTkButton(master=self.root, text="Wyszukaj zawodnika", command=self.wyszukaj_zawodnika)
        self.przycisk_wyszukaj_druzyne = customtkinter.CTkButton(master=self.root, text="Wyszukaj drużynę", command=self.wyszukaj_druzyne)
        self.przycisk_wyszukaj_sedziego = customtkinter.CTkButton(master=self.root, text="Wyszukaj sędziego", command=self.wyszukaj_sedziego)

        self.root.grid_anchor('center')
        self.przycisk_aktualizacji.grid(row=1, column=0, pady=5)
        self.przycisk_ustawien.grid(row=2, column=0, pady=5)
        self.przycisk_dane_ligi.grid(row=3, column=0, pady=5)
        self.przycisk_wyszukaj_zawodnika.grid(row=4, column=0, pady=5)
        self.przycisk_wyszukaj_druzyne.grid(row=5, column=0, pady=5)
        self.przycisk_wyszukaj_sedziego.grid(row=6, column=0, pady=5)
        
    def aktualizuj_dane(self):
        print("Aktualizacja danych")

    def otworz_ustawienia(self):
        print("Otwieranie ustawień")

    def otworz_dane_ligi(self):
        print("Otwieranie danych ligi")
        self.glowneOkno.setView("ligowe")

    def wyszukaj_zawodnika(self):
        print("Wyszukiwanie zawodnika")

    def wyszukaj_druzyne(self):
        print("Wyszukiwanie drużyny")

    def wyszukaj_sedziego(self):
        print("Wyszukiwanie sędziego")
        