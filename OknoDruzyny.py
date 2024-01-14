import tkinter as tk
from tkinter import ttk
import customtkinter
import pandas as pd
from WyciaganieDanych import teamMatches, listTeamSeasons, teamFutureMatches, teamSquad, findTeamLeague, leagueTable

class OknoDruzyny:
    def __init__(self, root, glowneOkno, team):
        self.root = root
        self.team = team
        self.root.geometry("1250x750")
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
        
        # select box do sezonow
        optionsSeason = listTeamSeasons(self.glowneOkno.dataMatchStats, self.team)
        self.seasonList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsSeason, command=self.changeSeason)
        self.seasonList.grid(row=3, column=0, pady=5, padx=10)
        self.seasonList.set(self.season)
        #self.seasonList.bind("<<ComboboxSelected>>", self.changeSeason)  
    
    
        #pobieranie danych
        data = self.glowneOkno.dataMatchStats
        self.league = findTeamLeague(data, self.team, self.season)
        dataTeamMatches = teamMatches(data, self.season, self.team)
        dataTeamFutureMatches = teamFutureMatches(self.glowneOkno.futureData, self.team)
        dataTeamSquad = teamSquad(self.glowneOkno.playerStatsData, self.team, self.season)
        dataLeagueTable = leagueTable(data, self.league, self.season)

        # tworzenie panelu widoku ligi
        tableFrame = customtkinter.CTkFrame(self.root)
        tableFrame.grid(row=0, column=1, sticky='nsew')
        
        # tabela zagranych meczy
        leagueTableLabel = customtkinter.CTkLabel(tableFrame, text=f"Zagrane mecze {self.team}", anchor="center", width=1070)
        leagueTableLabel.grid(row=0, column=0)
        tableLeague = self.createResultsTable(tableFrame, dataTeamMatches)
        tableLeague.grid(row=1, column=0, pady=5, padx=5)
        
        # frame na dwie tabele na dole
        tableFrameSmall = customtkinter.CTkFrame(tableFrame, fg_color='transparent')
        tableFrameSmall.grid(row=2, column=0, sticky='nsew')
        
        # tabela przyszlych meczy
        futureMatchesLabel = customtkinter.CTkLabel(tableFrameSmall, text=f"Przyszłe mecze {self.team}", anchor="n")
        futureMatchesLabel.grid(row=0, column=0, pady=10)
        tableFutureMatches = self.createFutureMatchesTable(tableFrameSmall, dataTeamFutureMatches)
        tableFutureMatches.grid(row=1, column=0, padx=10)
        
        # tabela zawodnikow
        teamSquadLabel = customtkinter.CTkLabel(tableFrameSmall, text=f"Zawodnicy {self.team}", anchor="n")
        teamSquadLabel.grid(row=0, column=1, pady=10)
        tableTeamSquad = self.createTeamSquadsTable(tableFrameSmall, dataTeamSquad)
        tableTeamSquad.grid(row=1, column=1, padx=10)
        
        # tabela ligowa
        leagueTableLabel = customtkinter.CTkLabel(tableFrameSmall, text=f"Tabela ligowa {self.league}", anchor="n")
        leagueTableLabel.grid(row=0, column=2, pady=10)
        tableLeagueTable = self.createLeagueTable(tableFrameSmall, dataLeagueTable)
        tableLeagueTable.grid(row=1, column=2, padx=10)
        
    def changeSeason(self, event=None):
        self.season = self.seasonList.get()
        self.windowView()

        
        
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
            if column in ['Gospodarz', 'Przyjezdny', 'Sędzia', 'Data']:
                tableResults.column(column, anchor="center", width=100)
            else:
                tableResults.column(column, anchor="center", width=50)
        
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
        
        frame = customtkinter.CTkFrame(root, height=500)
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tableResults = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        tableResults.pack(side=tk.LEFT, fill=tk.Y)
        tableResults["columns"] = list(data.columns)
        tableResults["show"] = "headings"
        tableResults["height"] = 20
        
        y_scrollbar.config(command=tableResults.yview)
        
        for column in tableResults["columns"]:
            if column in ['Gospodarz', 'Przyjezdny']:
                tableResults.column(column, anchor="center", width=130)
            else:
                tableResults.column(column, anchor="center", width=80)
        
        for col in data.columns:
            tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableResults, data))

        tableResults = self.glowneOkno.wypelnijTabele(tableResults, data)
        
        if(data.shape[0] < 20):
            for i in range(data.shape[0], 20-data.shape[0]):
                tableResults.insert("", "end", values=['','',''])
        
        tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableResults))
        
        return frame
    
    def createTeamSquadsTable(self, root, data):

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
            tableResults.column(column, anchor="center", width=130)
        
        for col in data.columns:
            tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableResults, data))

        tableResults = self.glowneOkno.wypelnijTabele(tableResults, data)
        tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableResults))
        
        return frame
    
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
                tableLeague.column(column, anchor="center", width=50)
        
        for col in data.columns:
            tableLeague.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableLeague, data))

        tableLeague = self.glowneOkno.wypelnijTabele(tableLeague, data)
        tableLeague.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableLeague))
        
        return tableLeague
    