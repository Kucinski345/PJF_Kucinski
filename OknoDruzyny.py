import tkinter as tk
from tkinter import ttk
import customtkinter
import pandas as pd
from WyciaganieDanych import teamMatches

class OknoDruzyny:
    def __init__(self, root, glowneOkno, team):
        self.root = root
        self.team = team
        self.root.geometry("1250x750")
        self.glowneOkno = glowneOkno
        self.season = '23_24'
        self.windowView()

        
    def windowView(self):
        
        self.root.grid_anchor('center')
        
        self.przyciskCofania = customtkinter.CTkButton(master=self.root, text="Powrót do menu", command=self.glowneOkno.przyciskCofania)
        self.przyciskCofania.grid(row=3, column=1, pady=5)
        
        
        
        # Tworzenie listy rozwijalnej
        options = ["23_24", "22_23", "21_22"]
        self.seasonList = ttk.Combobox(self.root, values=options)
        self.seasonList.grid(row=0, column=1, pady=5)
        self.seasonList.current(0)  # Ustawienie domyślnej opcji
        self.seasonList.bind("<<ComboboxSelected>>", self.onSelectedSeason)    
    
        
        self.data = self.glowneOkno.dataMatchStats
        self.dataTeamResult = teamMatches(self.data, self.season, self.team)
        self.dataTeamResult = self.dataTeamResult[['Gospodarz', 'Przyjezdny', 'homeGoals', 'awayGoals', 'date']]
        self.createTeamTable(self.root, self.dataTeamResult)
        
        
    def onSelectedSeason(self, event=None):
        self.season = self.seasonList.get()
        print("Wybrano:", self.season)
        
        self.dataTeamResult = teamMatches(self.data, self.season, self.team)
        self.dataTeamResult = self.dataTeamResult[['Gospodarz', 'Przyjezdny', 'homeGoals', 'awayGoals', 'date']]
        self.createTeamTable(self.root, self.dataTeamResult)
        
        
    def createTeamTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        self.tableLeague = ttk.Treeview(root)
        self.tableLeague["columns"] = list(data.columns)
        self.tableLeague["show"] = "headings"
        self.tableLeague.grid(row=2, column=1, pady=5)
        self.tableLeague["height"] = 20
        
        for column in self.tableLeague["columns"]:
            self.tableLeague.column(column, anchor="center", width=150)
        
        for col in data.columns:
            self.tableLeague.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, self.tableLeague, data))

        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, data)
        self.tableLeague.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, self.tableLeague))
        
    