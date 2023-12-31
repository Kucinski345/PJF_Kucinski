import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter

from WyciaganieDanych import leagueTable, leagueMatches

class OknoLigowe:
    def __init__(self, root, glowneOkno, league):
        self.root = root
        self.root.geometry("1250x750")
        self.league = league
        self.glowneOkno = glowneOkno
        self.season = '23_24'
        self.windowView()

        
    def windowView(self):
        
        frame = customtkinter.CTkFrame(self.root)
        frame.grid(row=2, column=1, pady=5, padx=5)
        self.przyciskCofania = customtkinter.CTkButton(master=frame, text="Powrót do menu", command=self.glowneOkno.przyciskCofania)
        self.przyciskPowrotu = customtkinter.CTkButton(master=frame, text="Cofnij", command=self.glowneOkno.przyciskPreviousView)

        frame.grid_anchor('center')
        self.przyciskCofania.grid(row=0, column=0, pady=5, padx=5)
        self.przyciskPowrotu.grid(row=0, column=1, pady=5, padx=5)
        
        data = self.glowneOkno.dataMatchStats
        dataLeagueTable = leagueTable(data, self.league, self.season)
        dataResultsTable = leagueMatches(data, self.season, self.league)
        dataResultsTable = dataResultsTable[['date', 'Gospodarz', 'Przyjezdny', 'homeGoals', 'awayGoals']]

        self.createLeagueTable(self.root, dataLeagueTable)
        self.createResultsTable(self.root, dataResultsTable)

    
    def createLeagueTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        self.tableLeague = ttk.Treeview(root)
        self.tableLeague["columns"] = list(data.columns)
        self.tableLeague["show"] = "headings"
        self.tableLeague.grid(row=0, column=2, pady=5, padx=5)
        self.tableLeague["height"] = 20
        
        for column in self.tableLeague["columns"]:
            self.tableLeague.column(column, anchor="center", width=100)
        
        for col in data.columns:
            self.tableLeague.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, self.tableLeague, data))

        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, data)
        self.tableLeague.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, self.tableLeague))
        
    def createResultsTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        

        frame = customtkinter.CTkFrame(self.root)
        frame.grid(row=0, column=0, pady=5, padx=5)
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tableResults = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set)
        self.tableResults.pack(side=tk.LEFT, fill=tk.Y)
        self.tableResults["columns"] = list(data.columns)
        self.tableResults["show"] = "headings"
        self.tableResults["height"] = 20
        
        y_scrollbar.config(command=self.tableResults.yview)
        
        for column in self.tableResults["columns"]:
            self.tableResults.column(column, anchor="center", width=100)
        
        for col in data.columns:
            self.tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, self.tableResults, data))

        self.tableResults = self.glowneOkno.wypelnijTabele(self.tableResults, data)
        self.tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, self.tableResults))



    

