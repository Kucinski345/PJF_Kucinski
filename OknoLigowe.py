import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter

from WyciaganieDanych import leagueTable, leagueMatches, listLeagues, listSeasons, futureMatches, leaguePlayersStats

class OknoLigowe:
    def __init__(self, root, glowneOkno, league):
        self.root = root
        self.root.geometry("1250x750")
        self.league = league
        self.glowneOkno = glowneOkno
        self.season = glowneOkno.defaultSeason
        self.windowView()

        
    def windowView(self):
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # tworzenie panelu menu
        buttonFrame = customtkinter.CTkFrame(self.root, width=100)
        buttonFrame.grid(row=0, column=0, sticky='ns')
        
        self.przyciskCofania = customtkinter.CTkButton(master=buttonFrame, text="Powrót do menu", command=self.glowneOkno.przyciskCofania)
        self.przyciskPowrotu = customtkinter.CTkButton(master=buttonFrame, text="Cofnij", command=self.glowneOkno.przyciskPreviousView)

        self.przyciskCofania.grid(row=0, column=0, pady=5, padx=10)
        self.przyciskPowrotu.grid(row=1, column=0, pady=5, padx=10)
        
        # select box do lig
        optionsLeague = listLeagues(self.glowneOkno.dataMatchStats)
        self.leagueList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsLeague, command=self.changeLeague)
        self.leagueList.grid(row=2, column=0, pady=5, padx=10)
        self.leagueList.set(self.league)
        #self.leagueList.bind("<<ComboboxSelected>>", self.changeLeague)  
        
        # select box do sezonow
        optionsSeason = listSeasons(self.glowneOkno.dataMatchStats, self.league)
        self.seasonList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsSeason, command=self.changeSeason)
        self.seasonList.grid(row=3, column=0, pady=5, padx=10)
        self.seasonList.set(self.season)
        #self.seasonList.bind("<<ComboboxSelected>>", self.changeSeason)  
        
        
        #pobieranie danych do wyswietlenia
        data = self.glowneOkno.dataMatchStats
        dataLeagueTable = leagueTable(data, self.league, self.season)
        dataResultsTable = leagueMatches(data, self.season, self.league)
        dataResultsTable = dataResultsTable[['Data', 'Gospodarz', 'Przyjezdny', "Wynik"]]
        dataFutureMatches = futureMatches(self.glowneOkno.futureData, self.league, self.season)
        dataPlayerStats = leaguePlayersStats(self.glowneOkno.playerStatsData, self.league, self.season)


        # tworzenie panelu widoku ligi
        tableFrame = customtkinter.CTkFrame(self.root)
        tableFrame.grid(row=0, column=1, sticky='nsew')
        
        # tabela ligowa
        leagueTableLabel = customtkinter.CTkLabel(tableFrame, text="Tabela ligowa", anchor="w")
        leagueTableLabel.grid(row=0, column=0)
        tableLeague = self.createLeagueTable(tableFrame, dataLeagueTable)
        tableLeague.grid(row=1, column=0, pady=5, padx=5)
        
        # wyniki meczow
        leagueResultsLabel = customtkinter.CTkLabel(tableFrame, text="Wyniki meczów", anchor="w")
        leagueResultsLabel.grid(row=2, column=0)
        tableResults = self.createResultsTable(tableFrame, dataResultsTable)
        tableResults.grid(row=3, column=0, pady=5, padx=5)
        
        # przyszle mecze
        leagueFutureMatchesLabel = customtkinter.CTkLabel(tableFrame, text="Przyszłe mecze", anchor="w")
        leagueFutureMatchesLabel.grid(row=2, column=1)
        tableFutureMatches = self.createFutureMatchesTable(tableFrame, dataFutureMatches)
        tableFutureMatches.grid(row=3, column=1, pady=5, padx=5)
        
        # statystyki zawodnikow
        leaguePlayerStatsLabel = customtkinter.CTkLabel(tableFrame, text="Statystyki zawodników", anchor="w")
        leaguePlayerStatsLabel.grid(row=0, column=1)
        tablePlayerStats = self.createPlayerStatsTable(tableFrame, dataPlayerStats)
        tablePlayerStats.grid(row=1, column=1, pady=5, padx=5)
        
        

    
    def changeLeague(self, event=None):
        self.league = self.leagueList.get()
        optionsSeason = listSeasons(self.glowneOkno.dataMatchStats, self.league)
        self.season = optionsSeason[0]
        self.windowView()
        
    def changeSeason(self, event=None):
        self.season = self.seasonList.get()
        self.windowView()


    def createLeagueTable(self, root, data):

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        

        tableLeague = ttk.Treeview(root)
        tableLeague["columns"] = list(data.columns)
        tableLeague["show"] = "headings"
        tableLeague["height"] = 20
        
        for column in tableLeague["columns"]:
            if column == 'Drużyna':
                tableLeague.column(column, anchor="center", width=100)
            else:
                tableLeague.column(column, anchor="center", width=62)
        
        for col in data.columns:
            tableLeague.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableLeague, data))

        tableLeague = self.glowneOkno.wypelnijTabele(tableLeague, data)
        tableLeague.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableLeague))
        
        return tableLeague
        
    def createResultsTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        frame = customtkinter.CTkFrame(root, height=100)
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tableResults = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        tableResults.pack(side=tk.LEFT, fill=tk.Y)
        tableResults["columns"] = list(data.columns)
        tableResults["show"] = "headings"
        tableResults["height"] = 10
        
        y_scrollbar.config(command=tableResults.yview)
        
        for column in tableResults["columns"]:
            tableResults.column(column, anchor="center", width=100)
        
        for col in data.columns:
            tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableResults, data))

        tableResults = self.glowneOkno.wypelnijTabele(tableResults, data)
        tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableResults))
        
        return frame

    def createFutureMatchesTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        frame = customtkinter.CTkFrame(root, height=100)
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tableResults = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        tableResults.pack(side=tk.LEFT, fill=tk.Y)
        tableResults["columns"] = list(data.columns)
        tableResults["show"] = "headings"
        tableResults["height"] = 10
        
        y_scrollbar.config(command=tableResults.yview)
        
        for column in tableResults["columns"]:
            tableResults.column(column, anchor="center", width=150)
        
        for col in data.columns:
            tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableResults, data))

        tableResults = self.glowneOkno.wypelnijTabele(tableResults, data)
        tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableResults))
        
        return frame
    
    def createPlayerStatsTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        frame = customtkinter.CTkFrame(root, height=100)
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tableResults = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        tableResults.pack(side=tk.LEFT, fill=tk.Y)
        tableResults["columns"] = list(data.columns)
        tableResults["show"] = "headings"
        tableResults["height"] = 20
        
        y_scrollbar.config(command=tableResults.yview)
        
        for column in tableResults["columns"]:
            if column == 'Zawodnik':
                tableResults.column(column, anchor="center", width=120)
            elif column in ('Drużyna', 'Czerwone'):
                tableResults.column(column, anchor="center", width=70)
            else:
                tableResults.column(column, anchor="center", width=45)
        
        for col in data.columns:
            tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableResults, data))

        tableResults = self.glowneOkno.wypelnijTabele(tableResults, data)
        tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableResults))
        
        return frame

    

