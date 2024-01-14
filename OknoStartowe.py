import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter


class OknoStartowe:
    def __init__(self, root, glowneOkno):
        self.root = root
        self.root.geometry("1250x750")
        self.windowView() 
        self.glowneOkno = glowneOkno
    
    def windowView(self):
        
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=0)
        
        self.przycisk_dane_ligi = customtkinter.CTkButton(master=self.root, text="Dane ligi", command=self.otworz_dane_ligi)
        self.przycisk_wyszukaj_zawodnika = customtkinter.CTkButton(master=self.root, text="Wyszukaj zawodnika", command=self.wyszukaj_zawodnika)
        self.przycisk_wyszukaj_druzyne = customtkinter.CTkButton(master=self.root, text="Wyszukaj drużynę", command=self.wyszukaj_druzyne)
        self.przycisk_wyszukaj_sedziego = customtkinter.CTkButton(master=self.root, text="Wyszukaj sędziego", command=self.wyszukaj_sedziego)
        #self.przycisk_wyszukaj_H2H = customtkinter.CTkButton(master=self.root, text="Wyszukaj H2H", command=self.wyszukaj_H2H)

        self.root.grid_anchor('center')
        self.przycisk_dane_ligi.grid(row=3, column=0, pady=5)
        self.przycisk_wyszukaj_zawodnika.grid(row=4, column=0, pady=5)
        self.przycisk_wyszukaj_druzyne.grid(row=5, column=0, pady=5)
        self.przycisk_wyszukaj_sedziego.grid(row=6, column=0, pady=5)
        #self.przycisk_wyszukaj_H2H.grid(row=7, column=0, pady=5)
        
    def otworz_dane_ligi(self):
        print("Otwieranie danych ligi")
        self.glowneOkno.setView("ligowe", 'PremierLeague')

    def wyszukaj_zawodnika(self):
        print("Wyszukiwanie zawodnika")
        self.glowneOkno.setView("searchPlayer")

    def wyszukaj_druzyne(self):
        print("Wyszukiwanie drużyny")
        self.glowneOkno.setView("searchTeam")

    def wyszukaj_sedziego(self):
        print("Wyszukiwanie sędziego")
        self.glowneOkno.setView("searchReferee")
        
    def wyszukaj_H2H(self):
        print("Wyszukiwanie H2H")
        