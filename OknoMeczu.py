import tkinter as tk
from tkinter import ttk
import customtkinter
import pandas as pd

from WyciaganieDanych import teamMatchSquad, matchStats, listLeagues, listPlayerSeasons, matchEvents, leaguePlayersStats, playerFinishedMatches

class OknoMeczu:
    def __init__(self, root, glowneOkno, dane):
        self.root = root
        self.root.geometry("1250x750")
        self.homeTeam = dane[1]
        self.awayTeam = dane[2]
        self.date = dane[0]
        self.season = glowneOkno.defaultSeason
        self.glowneOkno = glowneOkno
        self.windowView()

        
    def windowView(self):
        

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # tworzenie panelu menu
        buttonFrame = customtkinter.CTkFrame(self.root, width=100, fg_color="transparent")
        buttonFrame.grid(row=0, column=0, sticky='ns')
        
        self.przyciskCofania = customtkinter.CTkButton(master=buttonFrame, text="Powrót do menu", command=self.glowneOkno.przyciskCofania)
        self.przyciskPowrotu = customtkinter.CTkButton(master=buttonFrame, text="Cofnij", command=self.glowneOkno.przyciskPreviousView)

        self.przyciskCofania.grid(row=0, column=0, pady=5, padx=10)
        self.przyciskPowrotu.grid(row=1, column=0, pady=5, padx=10)
        

        #pobieranie danych do wyswietlenia
        data = self.glowneOkno.dataMatchStats
        matchDataStats = matchStats(data, self.date, self.homeTeam, self.awayTeam)
        matchHomeTeamSquad = teamMatchSquad(self.glowneOkno.matchSquadsData, self.date, self.homeTeam)
        matchAwayTeamSquad = teamMatchSquad(self.glowneOkno.matchSquadsData, self.date, self.awayTeam)
        matchEventsFirstHalfData, matchEventsSecondHalfData = matchEvents(self.glowneOkno.matchEventsData, self.date, self.homeTeam, self.awayTeam)
        
        # tworzenie panelu widoku ligi
        tableFrame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        tableFrame.grid(row=0, column=1, sticky='nsew')
        
        # tabela ligowa
        leagueTableLabel = customtkinter.CTkLabel(tableFrame, text="Statystyki meczu", anchor="w")
        leagueTableLabel.grid(row=0, column=0)
        tableLeague = self.createMatchStatsDisplay(tableFrame, matchDataStats)
        tableLeague.grid(row=1, column=0, pady=5, padx=5)
        

        
        leagueTableLabel = customtkinter.CTkLabel(tableFrame, text="Zdarzenia meczowe:", anchor="w")
        leagueTableLabel.grid(row=0, column=1)
        
        # frame na dwie tabele po prawej
        tableFrameSmall2 = customtkinter.CTkFrame(tableFrame, fg_color="transparent")
        tableFrameSmall2.grid(row=1, column=1, sticky='nsew')
        
        tableLeague = self.createResultsTable(tableFrameSmall2, matchEventsFirstHalfData)
        tableLeague.grid(row=0, column=0, pady=5, padx=5)
        
        tableLeague = self.createResultsTable(tableFrameSmall2, matchEventsSecondHalfData)
        tableLeague.grid(row=1, column=0, pady=5, padx=5)
        
        
        # frame na dwie tabele na dole
        tableFrameSmall = customtkinter.CTkFrame(tableFrame, fg_color="transparent")
        tableFrameSmall.grid(row=2, column=0, sticky='nsew')
        
        # tabela home squad
        futureMatchesLabel = customtkinter.CTkLabel(tableFrameSmall, text="Skład gospodarz", anchor="w")
        futureMatchesLabel.grid(row=2, column=0)
        matchHomeTeamSquad = matchHomeTeamSquad[['Drużyna','Zawodnik','Status']]
        tableFutureMatches = self.createTeamSquadTable(tableFrameSmall, matchHomeTeamSquad)
        tableFutureMatches.grid(row=3, column=0, pady=5, padx=5)
        
        # frame na dwie tabele na dole
        tableFrameSmall3 = customtkinter.CTkFrame(tableFrame, fg_color="transparent")
        tableFrameSmall3.grid(row=2, column=1, sticky='nsew')
        tableFrameSmall3.grid_anchor('center')
        
        # tabela away squad
        teamSquadLabel = customtkinter.CTkLabel(tableFrameSmall3, text="Skład przyjezdny", anchor="w")
        teamSquadLabel.grid(row=2, column=1)
        matchAwayTeamSquad = matchAwayTeamSquad[['Drużyna','Zawodnik','Status']]
        tableTeamSquad = self.createTeamSquadTable(tableFrameSmall3, matchAwayTeamSquad)
        tableTeamSquad.grid(row=3, column=1, pady=5, padx=5)
        
        
        
        
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
        
        frame = customtkinter.CTkFrame(root, height=100, fg_color="transparent")
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tableResults = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        tableResults.pack(side=tk.LEFT, fill=tk.Y)
        tableResults["columns"] = list(data.columns)
        tableResults["show"] = "headings"
        tableResults["height"] = min(data.shape[0], 8)
        
        y_scrollbar.config(command=tableResults.yview)
        
        for column in tableResults["columns"]:
            if column in ('Zawodnik', 'Gracz 1', 'Gracz 2'):
                tableResults.column(column, anchor="center", width=170)
            elif column in ('Drużyna', 'Zdarzenie'):
                tableResults.column(column, anchor="center", width=145)
            else:
                tableResults.column(column, anchor="center", width=50)
        
        for col in data.columns:
            tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableResults, data))

        tableResults = self.glowneOkno.wypelnijTabele(tableResults, data)
        tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableResults))
        
        return frame

    def createFutureTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        frame = customtkinter.CTkFrame(root, height=100, fg_color="transparent")
        
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
    
    def createPlayerStatsTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        frame = customtkinter.CTkFrame(root, height=100, fg_color="transparent")
        
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
    
    
    def createTeamSquadTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        frame = customtkinter.CTkFrame(root, height=100, fg_color="transparent")
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tableResults = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        tableResults.pack(side=tk.LEFT, fill=tk.Y)
        tableResults["columns"] = list(data.columns)
        tableResults["show"] = "headings"
        tableResults["height"] = 11
        
        y_scrollbar.config(command=tableResults.yview)
        
        for column in tableResults["columns"]:
            if column == 'Zawodnik':
                tableResults.column(column, anchor="center", width=120)
            elif column in ('Drużyna'):
                tableResults.column(column, anchor="center", width=120)
            else:
                tableResults.column(column, anchor="center", width=100)
        
        for col in data.columns:
            tableResults.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, tableResults, data))

        tableResults = self.glowneOkno.wypelnijTabele(tableResults, data)
        tableResults.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, tableResults))
        
        return frame
    
    def createMatchStatsDisplay(self, root, data):
        frame = customtkinter.CTkFrame(root, fg_color="transparent")
        
        date = data.iloc[0]['Data']
        homeTeam = data.iloc[0]['Gospodarz']
        awayTeam = data.iloc[0]['Przyjezdny']
        matchweek = data.iloc[0]['Kolejka']
        hour = data.iloc[0]['Godzina']
        homeTeam = data.iloc[0]['Gospodarz']
        awayTeam = data.iloc[0]['Przyjezdny']
        homeGoals = data.iloc[0]['homeGoals']
        awayGoals = data.iloc[0]['awayGoals']
        league = data.iloc[0]['Liga']
        season = data.iloc[0]['Sezon']
        referee = data.iloc[0]['Sędzia']
        homeLineup = data.iloc[0]['homeLineup']
        awayLineup = data.iloc[0]['awayLineup']
        homePossesion = data.iloc[0]['Posiadanie gospodarz'] * 100
        awayPossesion = data.iloc[0]['Posiadanie przyjezdny'] * 100
        
        label_text = f"{homeTeam} {homeGoals} : {awayGoals} {awayTeam}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=0, column=0)
        
        label_text = f"{league} - Sezon: {season}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=1, column=0)
        
        label_text = f"{date} - {hour} - Kolejka: {matchweek}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=2, column=0)
        
        label_text = f"Sędzia {referee}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=3, column=0)
    
        label_text = f"{homeLineup} - Ustawienie - {awayLineup}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=4, column=0)
        
        label_text = f"{homePossesion}% - Posiadanie - {awayPossesion}%"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=5, column=0)
        
        label_text = f"{data.iloc[0]['homePassingAccuracy']*100}% - Celnosć podań - {data.iloc[0]['awayPassingAccuracy']*100}%"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=6, column=0)
        
        label_text = f"{data.iloc[0]['Celnosć strzałów gospodarz']*100}% - Celnosć strzałów - {data.iloc[0]['Celnosć strzałów przyjezdny']*100}%"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=7, column=0)
        
        label_text = f"{data.iloc[0]['Faule gospodarz']} - Faule - {data.iloc[0]['Faule przyjezdny']}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=8, column=0)
        
        label_text = f"{data.iloc[0]['Rożne gospodarz']} - Rożne - {data.iloc[0]['Rożne przyjezdny']}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=9, column=0)
        
        label_text = f"{data.iloc[0]['homeOffsides']} - Spalone - {data.iloc[0]['awayOffsides']}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=10, column=0)
        
        return frame
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    