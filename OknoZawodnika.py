import pandas as pd
import tkinter as tk
from tkinter import ttk
import customtkinter

from WyciaganieDanych import playerFutureMatches, playerOverallStats, listLeagues, listPlayerSeasons, futureMatches, leaguePlayersStats, playerFinishedMatches

class OknoZawodnika:
    def __init__(self, root, glowneOkno, player):
        self.root = root
        self.root.geometry("1250x750")
        self.player = player
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
        
        # select box do sezonow
        optionsSeason = listPlayerSeasons(self.glowneOkno.playerStatsData, self.player)
        self.seasonList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsSeason, command=self.changeSeason)
        self.seasonList.grid(row=3, column=0, pady=5, padx=10)
        self.seasonList.set(self.season)
        #self.seasonList.bind("<<ComboboxSelected>>", self.changeSeason)  
        
        
        #pobieranie danych do wyswietlenia
        data = self.glowneOkno.playerStatsData
        dataFuture = self.glowneOkno.futureData
        dataPlayerMatches = playerFinishedMatches(data, self.glowneOkno.dataMatchStats, self.player, self.season)
        dataFutureMatches = playerFutureMatches(data, dataFuture, self.player)
        dataPlayerStats = playerOverallStats(data, self.player, self.season)
        
       
        # tworzenie panelu widoku ligi
        tableFrame = customtkinter.CTkFrame(self.root, fg_color="transparent")
        tableFrame.grid(row=0, column=1, sticky='nsew')
        
        # tabela mecze zawodnika
        leagueTableLabel = customtkinter.CTkLabel(tableFrame, text="Zagrane mecze", anchor="center")
        leagueTableLabel.grid(row=1, column=0)
        tableLeague = self.createResultsTable(tableFrame, dataPlayerMatches)
        tableLeague.grid(row=2, column=0, pady=5, padx=5)
        
        
        # frame na dwie tabele na dole
        tableFrameSmall = customtkinter.CTkFrame(tableFrame, fg_color="transparent")
        tableFrameSmall.grid(row=0, column=0, sticky='nsew')
        
        # tabela przyszle mecze
        leagueFutureMatchesLabel = customtkinter.CTkLabel(tableFrameSmall, text="Przyszłe mecze", anchor="center")
        leagueFutureMatchesLabel.grid(row=0, column=1)
        tableFutureMatches = self.createFutureTable(tableFrameSmall, dataFutureMatches)
        tableFutureMatches.grid(row=1, column=1, pady=5, padx=5)
        
        # tabela statystyki zawodnika
        leaguePlayerStatsLabel = customtkinter.CTkLabel(tableFrameSmall, text="Statystyki zawodnika", anchor="center", width=500)
        leaguePlayerStatsLabel.grid(row=0, column=0)
        tablePlayerStats = self.createPlayersStatsDisplay(tableFrameSmall, dataPlayerStats)
        tablePlayerStats.grid(row=1, column=0, pady=5, padx=5)
        
    
        
        
        
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
        tableResults["height"] = min(data.shape[0], 20)
        
        y_scrollbar.config(command=tableResults.yview)
        
        for column in tableResults["columns"]:
            tableResults.column(column, anchor="center", width=80)
        
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
    
    def createPlayersStatsDisplay(self, root, data):
        frame = customtkinter.CTkFrame(root, height=100, fg_color="transparent")
        
        player = data.iloc[0]['Zawodnik']
        label_text = f"Zawodnik: {player}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=0, column=0)
        
        team = data.iloc[0]['Drużyna']
        label_text = f"Drużyna: {team}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=1, column=0)
        
        age = data.iloc[0]['Wiek']
        age = age[:2]
        label_text = f"Wiek: {age} lat"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=2, column=0)
        
        shirtnumber = data.iloc[0]['shirtnumber']
        label_text = f"Numer koszulki: {shirtnumber}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=3, column=0)
        
        nationality = data.iloc[0]['Narodowość']
        label_text = f"Narodowość: {nationality}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=4, column=0)
        
        goals = data.iloc[0]['Gole']
        label_text = f"Gole: {goals}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=5, column=0)
        
        assists = data.iloc[0]['Asysty']
        label_text = f"Assysty: {assists}"
        label = customtkinter.CTkLabel(frame, text=label_text)
        label.grid(row=6, column=0)
        

        
        
        
        return frame
    
   
    
