import tkinter as tk
from tkinter import ttk
import customtkinter
import pandas as pd
from WyciaganieDanych import allTeamsTable

class OknoWyszukajDruzyne:
    def __init__(self, root, glowneOkno):
        self.root = root
        self.root.geometry("1250x750")
        self.glowneOkno = glowneOkno
        self.windowView()
        
    def windowView(self):
        self.przyciskCofania = customtkinter.CTkButton(master=self.root, text="Powrót do menu", command=self.glowneOkno.przyciskCofania)

        self.root.grid_anchor('center')
        self.przyciskCofania.grid(row=3, column=1, pady=5)
        
        self.data = self.glowneOkno.dataMatchStats
        self.dataTeamTable = allTeamsTable(self.data)
        self.displayedData = self.dataTeamTable
        self.createTeamTable(self.root, self.displayedData)
        

        labelTeamName = tk.Label(self.root, text="Nazwa:")
        labelTeamName.grid(row=0, column=1, pady=5)
        
        self.entryTeamName = tk.Entry(self.root)
        self.entryTeamName.grid(row=1, column=1, pady=5)
        
        self.entryTeamName.bind('<KeyRelease>', self.updateResults)
        

    def updateResults(self, event=None):
        searchName = self.entryTeamName.get()
        self.displayedData = self.dataTeamTable[self.dataTeamTable['Drużyna'].str.contains(searchName)]
        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, self.displayedData)
        
        
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
        