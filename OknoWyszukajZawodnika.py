import tkinter as tk
from tkinter import ttk
import customtkinter
import pandas as pd
from WyciaganieDanych import listLeagues, searchPlayers, listAllSeasons, listPositions

class OknoWyszukajZawodnika:
    def __init__(self, root, glowneOkno):
        self.root = root
        self.root.geometry("1250x750")
        self.glowneOkno = glowneOkno
        self.windowView()
        
    def windowView(self):
        
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_rowconfigure(0, weight=0)        

        buttonFrame = customtkinter.CTkFrame(self.root, width=100, fg_color="transparent")
        buttonFrame.grid(row=0, column=0, sticky='ns')
        
        self.przyciskCofania = customtkinter.CTkButton(master=buttonFrame, text="Powrót do menu", command=self.glowneOkno.przyciskCofania)

        buttonFrame.grid_anchor('center')
        self.przyciskCofania.grid(row=0, column=0, pady=5)
        
        # pobieranie danych
        self.data = self.glowneOkno.playerStatsData
        self.dataPlayers = searchPlayers(self.data, self.glowneOkno.defaultSeason)
        self.displayedData = self.dataPlayers
        frame = self.createPlayerTable(self.root, self.displayedData)
        frame.grid(row=0, column=1, pady=5, padx=10, sticky='n')

        # labale nazwa zawodnika
        labelPlayerName = customtkinter.CTkLabel(buttonFrame, text="Nazwa zawodnika:")
        labelPlayerName.grid(row=1, column=0, pady=5)
        self.entryPlayerName = customtkinter.CTkEntry(buttonFrame)
        self.entryPlayerName.grid(row=2, column=0, pady=5)
        self.entryPlayerName.bind('<KeyRelease>', self.updateResults)
        
        # labale nazwa druzyny
        labelTeamName = customtkinter.CTkLabel(buttonFrame, text="Nazwa drużyny:")
        labelTeamName.grid(row=7, column=0, pady=5)
        self.entryTeamName = customtkinter.CTkEntry(buttonFrame)
        self.entryTeamName.grid(row=8, column=0, pady=5)
        self.entryTeamName.bind('<KeyRelease>', self.updateResults)
        
        # combo box do ligi
        labelLeagueName = customtkinter.CTkLabel(buttonFrame, text="Nazwa ligi:")
        labelLeagueName.grid(row=3, column=0, pady=5)
        optionsLeague = listLeagues(self.glowneOkno.dataMatchStats)
        optionsLeague =  ('',) + optionsLeague
        self.leagueList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsLeague, command=self.selectLeague)
        self.leagueList.grid(row=4, column=0, pady=5)
        #self.leagueList.bind("<<ComboboxSelected>>", self.selectLeague)  
        
        # combo box do sezonow
        labelSeason = customtkinter.CTkLabel(buttonFrame, text="Sezon:")
        labelSeason.grid(row=5, column=0, pady=5)
        optionsSeason = listAllSeasons(self.glowneOkno.dataMatchStats)
        #optionsSeason =  ('',) + optionsSeason
        self.seasonList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsSeason, command=self.selectLeague)
        self.seasonList.grid(row=6, column=0, pady=5)
        #self.seasonList.bind("<<ComboboxSelected>>", self.selectLeague)  
        
        # combo box do pozycji
        labelPosition = customtkinter.CTkLabel(buttonFrame, text="Pozycja:")
        labelPosition.grid(row=9, column=0, pady=5)
        optionsPosition = listPositions(self.glowneOkno.playerStatsData)
        optionsPosition =  ('',) + optionsPosition
        self.positionList = customtkinter.CTkOptionMenu(buttonFrame, values=optionsPosition, command=self.selectLeague)
        self.positionList.grid(row=10, column=0, pady=5)
        #self.positionList.bind("<<ComboboxSelected>>", self.selectLeague)  
        
        # labale min age
        labelMinAge = customtkinter.CTkLabel(buttonFrame, text="Minimalny wiek:")
        labelMinAge.grid(row=11, column=0, pady=5)
        self.entryMinAge = customtkinter.CTkEntry(buttonFrame)
        self.entryMinAge.grid(row=12, column=0, pady=5)
        self.entryMinAge.bind('<KeyRelease>', self.updateResults)
        
        # labale max age
        labelMaxAge = customtkinter.CTkLabel(buttonFrame, text="Maksymalny wiek:")
        labelMaxAge.grid(row=13, column=0, pady=5)
        self.entryMaxAge = customtkinter.CTkEntry(buttonFrame)
        self.entryMaxAge.grid(row=14, column=0, pady=5)
        self.entryMaxAge.bind('<KeyRelease>', self.updateResults)
        
        # labale nationality
        labelNationality = customtkinter.CTkLabel(buttonFrame, text="Pochodzenie:")
        labelNationality.grid(row=15, column=0, pady=5)
        self.entryNationality = customtkinter.CTkEntry(buttonFrame)
        self.entryNationality.grid(row=16, column=0, pady=5)
        self.entryNationality.bind('<KeyRelease>', self.updateResults)
        

    def selectLeague(self, event=None):
        # filtrowanie sezonu
        seasonName = self.seasonList.get()
        if seasonName != '':
            self.displayedData = searchPlayers(self.data, seasonName)
        else:
            self.displayedData = self.dataPlayers
        
        # filtrowanie ligi
        leagueName = self.leagueList.get()
        if leagueName != '':
            self.displayedData = self.displayedData[self.displayedData['Liga'] == leagueName]
            
        # filtrowanie pozycji
        positionName = self.positionList.get()
        if positionName != '':
            self.displayedData = self.displayedData[self.displayedData['Pozycja'].str.contains(positionName, case=False)]

        # filtrowanie nazwy zawodnika
        playerName = self.entryPlayerName.get()
        self.displayedData = self.displayedData[self.displayedData['Zawodnik'].str.contains(playerName, case=False)]
        
        # filtrowanie nazwy druzyny
        teamName = self.entryTeamName.get()
        self.displayedData = self.displayedData[self.displayedData['Drużyna'].str.contains(teamName, case=False)]
        
        # filtrowanie minimalnego wieku
        minAge = self.entryMinAge.get()
        if minAge != '':
            self.displayedData = self.displayedData[self.displayedData['Wiek'].astype(int) >= int(minAge)]
        
        # filtrowanie maksymalnego wieku
        maxAge = self.entryMaxAge.get()
        if maxAge != '':
            self.displayedData = self.displayedData[self.displayedData['Wiek'].astype(int) <= int(maxAge)]
            
        # filtrowanie pochodzenia
        nationality = self.entryNationality.get()
        if nationality != '':
            self.displayedData = self.displayedData[self.displayedData['Narodowość'].str.contains(nationality, case=False)]
        
        # uzupelnienie tabeli
        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, self.displayedData)
        self.tableLeague["height"] = min(self.displayedData.shape[0], 25)


    def updateResults(self, event=None):
        # filtrowanie sezonu
        seasonName = self.seasonList.get()
        if seasonName != '':
            self.displayedData = searchPlayers(self.data, seasonName)
        else:
            self.displayedData = self.dataPlayers
        
        # filtrowanie ligi
        leagueName = self.leagueList.get()
        if leagueName != '':
            self.displayedData = self.displayedData[self.displayedData['Liga'] == leagueName]
        
        # filtrowanie nazwy zawodnika
        playerName = self.entryPlayerName.get()
        if playerName != '':
            self.displayedData = self.displayedData[self.displayedData['Zawodnik'].str.contains(playerName, case=False)]
        
        # filtrowanie nazwy druzyny
        teamName = self.entryTeamName.get()
        if teamName != '':
            self.displayedData = self.displayedData[self.displayedData['Drużyna'].str.contains(teamName, case=False)]
            
        # filtrowanie minimalnego wieku
        minAge = self.entryMinAge.get()
        if minAge != '':
            self.displayedData = self.displayedData[self.displayedData['Wiek'].astype(int) >= int(minAge)]
        
        # filtrowanie maksymalnego wieku
        maxAge = self.entryMaxAge.get()
        if maxAge != '':
            self.displayedData = self.displayedData[self.displayedData['Wiek'].astype(int) <= int(maxAge)]
            
        # filtrowanie pochodzenia
        nationality = self.entryNationality.get()
        if nationality != '':
            self.displayedData = self.displayedData[self.displayedData['Narodowość'].str.contains(nationality, case=False)]
            
        
        # uzupelnienie tabeli
        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, self.displayedData)
        self.tableLeague["height"] = min(self.displayedData.shape[0], 25)
        
        
    def createPlayerTable(self, root, data):

        style = ttk.Style()
        
        style.theme_use("clam")
        style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        #style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', foreground=[('!selected', '#E8E8E8')], background=[('!selected', '#323232')])
        style.map('Treeview.Heading', foreground=[('!selected', '#FFFFFF')], background=[('!selected', '#789789')])
        
        frame = customtkinter.CTkFrame(root, height=100)
        
        y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tableLeague = ttk.Treeview(frame, yscrollcommand=y_scrollbar.set, height=100)
        self.tableLeague.pack(side=tk.LEFT, fill=tk.Y)
        self.tableLeague["columns"] = list(data.columns)
        self.tableLeague["show"] = "headings"
        self.tableLeague["height"] = min(data.shape[0], 31)
        
        y_scrollbar.config(command=self.tableLeague.yview)
        
        for column in self.tableLeague["columns"]:
            if column == 'Zawodnik':
                self.tableLeague.column(column, anchor="center", width=180)
            elif column in ('Wiek', 'Pozycja'):
                self.tableLeague.column(column, anchor="center", width=70)
            else:
                self.tableLeague.column(column, anchor="center", width=150)
        
        for col in data.columns:
            self.tableLeague.heading(col, text=col, command=lambda c=col: self.glowneOkno.sortTable(c, self.tableLeague, data))

        self.tableLeague = self.glowneOkno.wypelnijTabele(self.tableLeague, data)
        self.tableLeague.bind("<ButtonRelease-1>", lambda event: self.glowneOkno.showValue(event, self.tableLeague))
        
        return frame
        
